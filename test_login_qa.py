"""
QA Test Script for Login Page Redesign
Tests: Design, Functionality, Responsiveness, Error Handling
"""

import asyncio
from playwright.async_api import async_playwright
import os
from datetime import datetime

# Test configuration
BASE_URL = "http://localhost:8000"
LOGIN_URL = f"{BASE_URL}/login/"
SCREENSHOTS_DIR = "C:\\Projetos Claude Code\\sge\\qa_screenshots"

# Create screenshots directory
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

async def run_qa_tests():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)

        print("\n" + "="*80)
        print("QA AUDIT - Login Page Redesign")
        print("="*80 + "\n")

        # =====================================================
        # TEST 1: Initial Page Load - Desktop View
        # =====================================================
        print("[TEST 1] Loading login page - Desktop viewport (1280x800)...")
        context = await browser.new_context(viewport={'width': 1280, 'height': 800})
        page = await context.new_page()

        # Navigate to login page
        await page.goto(LOGIN_URL)
        await page.wait_for_load_state('networkidle')

        # Take screenshot
        screenshot_path = os.path.join(SCREENSHOTS_DIR, "01_login_desktop_initial.png")
        await page.screenshot(path=screenshot_path, full_page=True)
        print(f"   Screenshot saved: {screenshot_path}")

        # Check console messages
        console_messages = []
        page.on('console', lambda msg: console_messages.append(f"[{msg.type}] {msg.text}"))

        # Reload to capture console
        await page.reload()
        await page.wait_for_load_state('networkidle')
        await asyncio.sleep(1)

        print(f"   Console messages: {len(console_messages)} entries")
        for msg in console_messages:
            print(f"      {msg}")

        # =====================================================
        # TEST 2: Visual Design Audit
        # =====================================================
        print("\n[TEST 2] Auditing visual design elements...")

        # Check for key design elements
        logo_icon = await page.query_selector('svg')
        print(f"   Logo icon present: {logo_icon is not None}")

        title = await page.query_selector('h1')
        title_text = await title.inner_text() if title else None
        print(f"   Title text: '{title_text}'")

        subtitle = await page.query_selector('p.text-slate-400')
        subtitle_text = await subtitle.inner_text() if subtitle else None
        print(f"   Subtitle: '{subtitle_text}'")

        card = await page.query_selector('.bg-slate-800\\/50')
        print(f"   Glassmorphism card present: {card is not None}")

        gradient_button = await page.query_selector('.bg-gradient-to-r')
        print(f"   Gradient button present: {gradient_button is not None}")

        # Check background gradient
        body_classes = await page.evaluate('document.body.className')
        has_gradient = 'bg-gradient-to-br' in body_classes
        print(f"   Background gradient applied: {has_gradient}")

        # =====================================================
        # TEST 3: Test Error Flow - Invalid Credentials
        # =====================================================
        print("\n[TEST 3] Testing error flow with invalid credentials...")

        # Fill form with invalid credentials
        await page.fill('input[name="username"]', 'wrong_user')
        await page.fill('input[name="password"]', 'wrong_password')

        screenshot_path = os.path.join(SCREENSHOTS_DIR, "02_login_filled_invalid.png")
        await page.screenshot(path=screenshot_path, full_page=True)
        print(f"   Screenshot (filled form): {screenshot_path}")

        # Submit form
        await page.click('button[type="submit"]')
        await page.wait_for_load_state('networkidle')
        await asyncio.sleep(0.5)

        # Check for error message
        error_div = await page.query_selector('.bg-red-900\\/30')
        error_present = error_div is not None
        print(f"   Error message displayed: {error_present}")

        if error_present:
            error_text = await error_div.inner_text()
            print(f"   Error text: '{error_text.strip()}'")

        screenshot_path = os.path.join(SCREENSHOTS_DIR, "03_login_error_state.png")
        await page.screenshot(path=screenshot_path, full_page=True)
        print(f"   Screenshot (error state): {screenshot_path}")

        # =====================================================
        # TEST 4: Test Successful Login
        # =====================================================
        print("\n[TEST 4] Testing successful login flow...")

        # Clear and fill with valid credentials
        await page.fill('input[name="username"]', 'admin')
        await page.fill('input[name="password"]', 'admin')

        screenshot_path = os.path.join(SCREENSHOTS_DIR, "04_login_filled_valid.png")
        await page.screenshot(path=screenshot_path, full_page=True)
        print(f"   Screenshot (valid credentials): {screenshot_path}")

        # Submit form
        await page.click('button[type="submit"]')
        await page.wait_for_load_state('networkidle')
        await asyncio.sleep(1)

        # Check if redirected
        current_url = page.url
        print(f"   Current URL after login: {current_url}")
        print(f"   Login successful: {current_url != LOGIN_URL}")

        screenshot_path = os.path.join(SCREENSHOTS_DIR, "05_post_login_page.png")
        await page.screenshot(path=screenshot_path, full_page=True)
        print(f"   Screenshot (post-login): {screenshot_path}")

        # Close this context
        await context.close()

        # =====================================================
        # TEST 5: Responsiveness - Mobile (375x812)
        # =====================================================
        print("\n[TEST 5] Testing mobile responsiveness (375x812)...")
        context_mobile = await browser.new_context(viewport={'width': 375, 'height': 812})
        page_mobile = await context_mobile.new_page()

        await page_mobile.goto(LOGIN_URL)
        await page_mobile.wait_for_load_state('networkidle')

        screenshot_path = os.path.join(SCREENSHOTS_DIR, "06_login_mobile_375.png")
        await page_mobile.screenshot(path=screenshot_path, full_page=True)
        print(f"   Screenshot (mobile): {screenshot_path}")

        # Check if elements are visible and properly sized
        card_mobile = await page_mobile.query_selector('.bg-slate-800\\/50')
        if card_mobile:
            box = await card_mobile.bounding_box()
            print(f"   Card width on mobile: {box['width']}px")
            print(f"   Card fits viewport: {box['width'] <= 375}")

        await context_mobile.close()

        # =====================================================
        # TEST 6: Responsiveness - Tablet (768x1024)
        # =====================================================
        print("\n[TEST 6] Testing tablet responsiveness (768x1024)...")
        context_tablet = await browser.new_context(viewport={'width': 768, 'height': 1024})
        page_tablet = await context_tablet.new_page()

        await page_tablet.goto(LOGIN_URL)
        await page_tablet.wait_for_load_state('networkidle')

        screenshot_path = os.path.join(SCREENSHOTS_DIR, "07_login_tablet_768.png")
        await page_tablet.screenshot(path=screenshot_path, full_page=True)
        print(f"   Screenshot (tablet): {screenshot_path}")

        await context_tablet.close()

        # =====================================================
        # TEST 7: Responsiveness - Wide Desktop (1920x1080)
        # =====================================================
        print("\n[TEST 7] Testing wide desktop responsiveness (1920x1080)...")
        context_wide = await browser.new_context(viewport={'width': 1920, 'height': 1080})
        page_wide = await context_wide.new_page()

        await page_wide.goto(LOGIN_URL)
        await page_wide.wait_for_load_state('networkidle')

        screenshot_path = os.path.join(SCREENSHOTS_DIR, "08_login_wide_1920.png")
        await page_wide.screenshot(path=screenshot_path, full_page=True)
        print(f"   Screenshot (wide desktop): {screenshot_path}")

        await context_wide.close()

        # =====================================================
        # TEST 8: Accessibility Audit
        # =====================================================
        print("\n[TEST 8] Accessibility audit...")
        context_a11y = await browser.new_context(viewport={'width': 1280, 'height': 800})
        page_a11y = await context_a11y.new_page()

        await page_a11y.goto(LOGIN_URL)
        await page_a11y.wait_for_load_state('networkidle')

        # Check for labels
        username_label = await page_a11y.query_selector('label[for="username"]')
        password_label = await page_a11y.query_selector('label[for="password"]')
        print(f"   Username label present: {username_label is not None}")
        print(f"   Password label present: {password_label is not None}")

        # Check for required attributes
        username_input = await page_a11y.query_selector('input[name="username"]')
        password_input = await page_a11y.query_selector('input[name="password"]')

        if username_input:
            is_required = await username_input.get_attribute('required')
            has_autofocus = await username_input.get_attribute('autofocus')
            print(f"   Username field required: {is_required is not None}")
            print(f"   Username field autofocus: {has_autofocus is not None}")

        if password_input:
            is_required = await password_input.get_attribute('required')
            input_type = await password_input.get_attribute('type')
            print(f"   Password field required: {is_required is not None}")
            print(f"   Password field type: {input_type}")

        # Check keyboard navigation
        print("\n   Testing keyboard navigation...")
        await page_a11y.keyboard.press('Tab')
        focused_element = await page_a11y.evaluate('document.activeElement.tagName')
        print(f"   First tab focus: {focused_element}")

        await page_a11y.keyboard.press('Tab')
        focused_element = await page_a11y.evaluate('document.activeElement.tagName')
        print(f"   Second tab focus: {focused_element}")

        await context_a11y.close()

        # =====================================================
        # TEST 9: Form Field Validation
        # =====================================================
        print("\n[TEST 9] Testing form field validation...")
        context_validation = await browser.new_context(viewport={'width': 1280, 'height': 800})
        page_validation = await context_validation.new_page()

        await page_validation.goto(LOGIN_URL)
        await page_validation.wait_for_load_state('networkidle')

        # Try to submit empty form (HTML5 validation)
        print("   Testing empty form submission...")
        await page_validation.click('button[type="submit"]')
        await asyncio.sleep(0.5)

        # Check if still on login page (validation prevented submission)
        current_url = page_validation.url
        print(f"   HTML5 validation working: {current_url == LOGIN_URL}")

        await context_validation.close()

        # =====================================================
        # TEST 10: Button Hover State
        # =====================================================
        print("\n[TEST 10] Testing interactive states...")
        context_hover = await browser.new_context(viewport={'width': 1280, 'height': 800})
        page_hover = await context_hover.new_page()

        await page_hover.goto(LOGIN_URL)
        await page_hover.wait_for_load_state('networkidle')

        # Hover over submit button
        submit_button = await page_hover.query_selector('button[type="submit"]')
        await submit_button.hover()
        await asyncio.sleep(0.3)

        screenshot_path = os.path.join(SCREENSHOTS_DIR, "09_button_hover_state.png")
        await page_hover.screenshot(path=screenshot_path, full_page=True)
        print(f"   Screenshot (button hover): {screenshot_path}")

        # Focus on input field
        username_input = await page_hover.query_selector('input[name="username"]')
        await username_input.click()
        await asyncio.sleep(0.3)

        screenshot_path = os.path.join(SCREENSHOTS_DIR, "10_input_focus_state.png")
        await page_hover.screenshot(path=screenshot_path, full_page=True)
        print(f"   Screenshot (input focus): {screenshot_path}")

        await context_hover.close()

        print("\n" + "="*80)
        print("QA AUDIT COMPLETED")
        print(f"Screenshots saved to: {SCREENSHOTS_DIR}")
        print("="*80 + "\n")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run_qa_tests())
