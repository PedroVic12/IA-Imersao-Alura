from playwright.sync_api import sync_playwright, Page, Browser
import time

class ChromeAutomation:
    def __init__(self):
        self.playwright = sync_playwright().start()
        self.browser: Browser = self.playwright.chromium.launch(channel="chrome", headless=False)
        self.page: Page = self.browser.new_page()

    def navigate_to_url(self, url: str):
        """Navega para uma URL específica."""
        self.page.goto(url)
        print(f"Navegou para: {url}")

    def take_screenshot(self, path: str):
        """Tira um screenshot da página atual."""
        self.page.screenshot(path=path)
        print(f"Screenshot salvo em: {path}")

    def fill_form(self, selector: str, text: str):
        """Preenche um campo de formulário."""
        self.page.fill(selector, text)
        print(f"Preencheu o campo {selector} com: {text}")

    def click_element(self, selector: str):
        """Clica em um elemento na página."""
        self.page.click(selector)
        print(f"Clicou no elemento: {selector}")

    def scroll_page(self, pixels: int):
        """Rola a página por um número específico de pixels."""
        self.page.evaluate(f"window.scrollBy(0, {pixels})")
        print(f"Rolou a página por {pixels} pixels")

    def wait_for_element(self, selector: str, timeout: int = 30000):
        """Espera por um elemento aparecer na página."""
        self.page.wait_for_selector(selector, timeout=timeout)
        print(f"Elemento {selector} apareceu na página")

    def extract_text(self, selector: str) -> str:
        """Extrai o texto de um elemento."""
        text = self.page.text_content(selector)
        print(f"Texto extraído de {selector}: {text}")
        return text

    def close(self):
        """Fecha o navegador e encerra a sessão."""
        self.browser.close()
        self.playwright.stop()
        print("Navegador fechado e sessão encerrada")

# Exemplo de uso
if __name__ == "__main__":
    chrome = ChromeAutomation()
    
    try:
        chrome.navigate_to_url("https://globoplay.globo.com/")
        time.sleep(5)
        
        chrome.take_screenshot("exemplo.png")
        
        chrome.fill_form("input[name='search']", "teste de automação")
        
        chrome.click_element("button[type='submit']")
        
        chrome.scroll_page(500)
        
        chrome.wait_for_element(".result-item")
        
        text = chrome.extract_text(".result-item")
        print(f"Texto extraído: {text}")
        
    finally:
        chrome.close()