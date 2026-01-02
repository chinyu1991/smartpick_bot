# selenium_utils.py
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple, Union

from selenium.webdriver.remote.webdriver import WebDriver, WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException

Locator = Tuple[By, str]

@dataclass
class SeleniumHelper:
    driver: WebDriver
    default_timeout: int = 10

    def wait(self, timeout: Optional[int] = None) -> WebDriverWait:
        return WebDriverWait(self.driver, timeout or self.default_timeout)

    # -------- Find / Wait --------
    def find(self, loc: Locator, timeout: Optional[int] = None) -> WebElement:
        """等到元素存在（presence）并返回"""
        return self.wait(timeout).until(EC.presence_of_element_located(loc))

    def find_visible(self, loc: Locator, timeout: Optional[int] = None) -> WebElement:
        """等到元素可见并返回"""
        return self.wait(timeout).until(EC.visibility_of_element_located(loc))

    def find_clickable(self, loc: Locator, timeout: Optional[int] = None) -> WebElement:
        """等到元素可点击并返回"""
        return self.wait(timeout).until(EC.element_to_be_clickable(loc))

    def wait_gone(self, loc: Locator, timeout: Optional[int] = None) -> bool:
        """等待元素消失（例如 loading）"""
        return self.wait(timeout).until(EC.invisibility_of_element_located(loc))

    def exists(self, loc: Locator, timeout: int = 2) -> bool:
        """短等待判断元素是否存在/可见（按需改为 presence/visibility）"""
        try:
            self.find(loc, timeout=timeout)
            return True
        except TimeoutException:
            return False

    # -------- Click --------
    def click(self, loc: Locator, timeout: Optional[int] = None, js_fallback: bool = True) -> WebElement:
        """稳健点击：优先正常点击，失败可用 JS 兜底"""
        el = self.find_clickable(loc, timeout=timeout)
        try:
            self.scroll_into_view(el)
            el.click()
            return el
        except Exception:
            if not js_fallback:
                raise
            self.driver.execute_script("arguments[0].click();", el)
            return el

    # -------- Input --------
    def input_text(
        self,
        loc: Locator,
        text: str,
        timeout: Optional[int] = None,
        clear: bool = True,
        press_enter: bool = False,
        slow: bool = False,
        slow_delay: float = 0.08,
        js_fallback: bool = False,
    ) -> WebElement:
        """通用输入：可清空/慢打字/回车/JS 兜底（适合 React/Vue）"""
        el = self.find_clickable(loc, timeout=timeout)
        self.scroll_into_view(el)
        self.driver.execute_script("arguments[0].focus();", el)
        try:
            el.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", el)

        if clear:
            try:
                el.clear()
            except Exception:
                # 有些输入框 clear 不稳定，兜底：Ctrl/Command + A 删除
                el.send_keys(Keys.COMMAND, "a")
                el.send_keys(Keys.BACKSPACE)

        if js_fallback:
            self.driver.execute_script(
                """
                arguments[0].value = arguments[1];
                arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
                arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
                """,
                el,
                text,
            )
        else:
            if slow:
                import time
                for ch in text:
                    el.send_keys(ch)
                    time.sleep(slow_delay)
            else:
                el.send_keys(text)

        if press_enter:
            el.send_keys(Keys.ENTER)

        return el

    # -------- Text / Attr --------
    def get_text(self, loc: Locator, timeout: Optional[int] = None) -> str:
        el = self.find_visible(loc, timeout=timeout)
        return el.text.strip()

    def get_value(self, loc: Locator, timeout: Optional[int] = None) -> str:
        el = self.find(loc, timeout=timeout)
        return (el.get_attribute("value") or "").strip()

    # -------- Select (dropdown) --------
    def select_by_value(self, loc: Locator, value: str, timeout: Optional[int] = None) -> None:
        el = self.find(loc, timeout=timeout)
        Select(el).select_by_value(value)

    def select_by_text(self, loc: Locator, text: str, timeout: Optional[int] = None) -> None:
        el = self.find(loc, timeout=timeout)
        Select(el).select_by_visible_text(text)

    # -------- Upload file --------
    def upload_file(self, loc: Locator, file_path: Union[str, Path], timeout: Optional[int] = None) -> WebElement:
        """input[type=file] 直接 send_keys 本地文件路径即可"""
        path = str(Path(file_path).expanduser().resolve())
        el = self.find(loc, timeout=timeout)
        el.send_keys(path)
        return el

    # -------- Iframe --------
    def switch_to_frame(self, frame_loc: Locator, timeout: Optional[int] = None) -> None:
        """切进 iframe（用 locator 找 iframe 元素）"""
        self.driver.switch_to.default_content()
        frame_el = self.find(frame_loc, timeout=timeout)
        self.driver.switch_to.frame(frame_el)

    def switch_to_default(self) -> None:
        self.driver.switch_to.default_content()

    # -------- Scroll / Screenshot --------
    def scroll_into_view(self, el: WebElement) -> None:
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)

    def screenshot(self, path: Union[str, Path]) -> str:
        """保存截图，返回实际路径"""
        p = Path(path).expanduser()
        # 自动补 .png
        if p.suffix.lower() != ".png":
            p = p.with_suffix(".png")

        p.parent.mkdir(parents=True, exist_ok=True)
        self.driver.save_screenshot(str(p))
        return str(p)

    # -------- Retry wrapper (处理 stale) --------
    def retry_on_stale(self, func, retries: int = 2):
        """DOM 刷新导致 StaleElementReference 时重试"""
        for i in range(retries + 1):
            try:
                return func()
            except StaleElementReferenceException:
                if i == retries:
                    raise
