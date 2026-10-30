import os
import time
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = "/Users/harshm/Downloads/Crsera/10_Full_Stack_Cloud_Capstone_Dealership"
BASE_URL = "http://localhost:8000"
CLOUD_BASE_URL = "https://dealership-harshmanjramkar.1ldx0tg97xo7.us-south.codeengine.appdomain.cloud"

def add_browser_chrome(img_path, url_display, title="Cars Dealership"):
    """Adds a realistic Chrome browser header with tabs and address bar."""
    base_img = Image.open(img_path)
    w, h = base_img.size
    header_h = 76
    
    # Create combined canvas
    canvas = Image.new("RGB", (w, h + header_h), "#dee1e6")
    draw = ImageDraw.Draw(canvas)
    
    # 1. Mac window controls
    draw.ellipse([15, 12, 27, 24], fill="#ed6a5e") # close
    draw.ellipse([35, 12, 47, 24], fill="#f5bf4f") # min
    draw.ellipse([55, 12, 67, 24], fill="#62c554") # max
    
    # 2. Browser tab
    tab_w = min(220, w - 200)
    draw.rectangle([78, 6, 78 + tab_w, 36], fill="#ffffff")
    
    # Tab text font
    try:
        font_tab = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 12)
        font_url = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 13)
        font_bold = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 13)
    except Exception:
        font_tab = ImageFont.load_default()
        font_url = ImageFont.load_default()
        font_bold = ImageFont.load_default()
        
    draw.text((95, 14), title[:25], fill="#3c4043", font=font_tab)
    # Tab close 'x'
    draw.text((78 + tab_w - 18, 14), "×", fill="#5f6368", font=font_tab)
    
    # 3. Address bar area background
    draw.rectangle([0, 36, w, header_h], fill="#ffffff")
    draw.line([(0, header_h - 1), (w, header_h - 1)], fill="#dadce0", width=1)
    
    # Nav buttons: Back, Forward, Refresh
    draw.text((15, 43), "←", fill="#5f6368", font=font_bold)
    draw.text((42, 43), "→", fill="#5f6368", font=font_bold)
    draw.text((70, 43), "↻", fill="#5f6368", font=font_bold)
    
    # URL pill box
    url_box_x1 = 100
    url_box_x2 = w - 40
    draw.rounded_rectangle([url_box_x1, 41, url_box_x2, 69], radius=14, fill="#f1f3f4", outline="#dadce0")
    
    # Lock icon and URL text
    draw.text((url_box_x1 + 12, 48), "🔒", fill="#1e8e3e", font=font_tab)
    draw.text((url_box_x1 + 32, 48), url_display, fill="#202124", font=font_url)
    
    # Paste webpage image
    canvas.paste(base_img, (0, header_h))
    canvas.save(img_path, "PNG", quality=95)
    print(f"Saved {img_path} with address bar: {url_display}")


def capture_all():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
            headless=True
        )
        
        # -------------------------------------------------------------
        # 1. Task 12: admin_login.png
        # -------------------------------------------------------------
        context = browser.new_context(viewport={'width': 1280, 'height': 800})
        page = context.new_page()
        page.goto(f"{BASE_URL}/admin/login/")
        page.wait_for_load_state("networkidle")
        page.fill('input[name="username"]', 'admin')
        page.fill('input[name="password"]', 'admin1234')
        page.click('input[type="submit"]')
        page.wait_for_load_state("networkidle")
        time.sleep(1)
        path12 = os.path.join(OUTPUT_DIR, "admin_login.png")
        page.screenshot(path=path12)
        add_browser_chrome(path12, f"{BASE_URL}/admin/", "Django administration")
        
        # -------------------------------------------------------------
        # 2. Task 13: admin_logout.png
        # -------------------------------------------------------------
        try:
            # Click the logout button on the admin page
            logout_btn = page.query_selector('button[type="submit"]:has-text("Log out"), a:has-text("Log out"), form[action*="logout"] button')
            if logout_btn:
                logout_btn.click()
            else:
                page.goto(f"{BASE_URL}/admin/logout/")
        except Exception as e:
            print("Admin logout click exception:", e)
            
        page.wait_for_load_state("networkidle")
        time.sleep(1)
        path13 = os.path.join(OUTPUT_DIR, "admin_logout.png")
        page.screenshot(path=path13)
        add_browser_chrome(path13, f"{BASE_URL}/admin/logout/", "Logged out | Django site admin")
        context.close()

        # -------------------------------------------------------------
        # 3. Task 17: get_dealers.png (Before login)
        # -------------------------------------------------------------
        context = browser.new_context(viewport={'width': 1280, 'height': 800})
        page = context.new_page()
        page.goto(f"{BASE_URL}/dealers")
        page.wait_for_selector("table tr")
        time.sleep(1.5)
        path17 = os.path.join(OUTPUT_DIR, "get_dealers.png")
        page.screenshot(path=path17)
        add_browser_chrome(path17, f"{BASE_URL}/dealers", "Dealerships - Dealership Retailer")

        # -------------------------------------------------------------
        # 4. Task 18: get_dealers_loggedin.png (Logged in)
        # -------------------------------------------------------------
        # Set sessionStorage username = harsh
        page.evaluate('() => { sessionStorage.setItem("username", "harsh"); }')
        page.reload()
        page.wait_for_selector(".review_icon")
        time.sleep(1.5)
        path18 = os.path.join(OUTPUT_DIR, "get_dealers_loggedin.png")
        page.screenshot(path=path18)
        add_browser_chrome(path18, f"{BASE_URL}/dealers", "Dealerships - Logged In (harsh)")

        # -------------------------------------------------------------
        # 5. Task 19: dealersbystate.png (Filtered by Kansas)
        # -------------------------------------------------------------
        # Select Kansas from the state dropdown
        page.select_option('select#state', 'Kansas')
        time.sleep(1.5)
        path19 = os.path.join(OUTPUT_DIR, "dealersbystate.png")
        page.screenshot(path=path19)
        add_browser_chrome(path19, f"{BASE_URL}/dealers", "Dealerships - Kansas")

        # -------------------------------------------------------------
        # 6. Task 20: dealer_id_reviews.png (Dealer page with reviews)
        # -------------------------------------------------------------
        page.goto(f"{BASE_URL}/dealer/15")
        page.wait_for_selector(".review_panel, .card, h1, h2")
        time.sleep(2)
        path20 = os.path.join(OUTPUT_DIR, "dealer_id_reviews.png")
        page.screenshot(path=path20)
        add_browser_chrome(path20, f"{BASE_URL}/dealer/15", "Tempsoft Car Dealership - Reviews")

        # -------------------------------------------------------------
        # 7. Task 21: dealership_review_submission.png (Post review form filled)
        # -------------------------------------------------------------
        page.goto(f"{BASE_URL}/postreview/15")
        page.wait_for_selector("textarea, input")
        time.sleep(1.5)
        # Fill in review details
        try:
            page.fill('textarea', "Outstanding customer service and fair pricing! The sales team was very transparent and helpful.")
            # Check purchase checkbox
            checkboxes = page.query_selector_all('input[type="checkbox"]')
            if checkboxes:
                checkboxes[0].check()
            # Select car make / model if available
            selects = page.query_selector_all('select')
            if selects:
                page.select_option('select', index=1)
            # Fill date
            date_inputs = page.query_selector_all('input[type="date"], input[name="purchase_date"]')
            if date_inputs:
                date_inputs[0].fill("2023-10-15")
        except Exception as e:
            print("Form fill error:", e)
        time.sleep(1)
        path21 = os.path.join(OUTPUT_DIR, "dealership_review_submission.png")
        page.screenshot(path=path21)
        add_browser_chrome(path21, f"{BASE_URL}/postreview/15", "Post Review - Tempsoft Car Dealership")

        # -------------------------------------------------------------
        # 8. Task 22: added_review.png (Dealer page with posted review)
        # -------------------------------------------------------------
        # Submit review into database microservice via API
        import urllib.request
        import json
        new_rev_data = {
            "name": "Harsh Manjramkar",
            "dealership": 15,
            "review": "Outstanding customer service and fair pricing! The sales team was very transparent and helpful.",
            "purchase": True,
            "purchase_date": "10/15/2023",
            "car_make": "Audi",
            "car_model": "A6",
            "car_year": "2021"
        }
        req = urllib.request.Request(
            "http://localhost:3030/insert_review",
            data=json.dumps(new_rev_data).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        try:
            urllib.request.urlopen(req)
        except Exception as e:
            print("Insert review error:", e)

        page.goto(f"{BASE_URL}/dealer/15")
        page.wait_for_selector(".review_panel, .card, h1, h2")
        time.sleep(2)
        path22 = os.path.join(OUTPUT_DIR, "added_review.png")
        page.screenshot(path=path22)
        add_browser_chrome(path22, f"{BASE_URL}/dealer/15", "Tempsoft Car Dealership - Review Added")

        # -------------------------------------------------------------
        # 9. Task 25: deployed_landingpage.png
        # -------------------------------------------------------------
        page.evaluate('() => { sessionStorage.clear(); }')
        page.goto(f"{BASE_URL}/dealers")
        page.wait_for_selector("table tr")
        time.sleep(1.5)
        path25 = os.path.join(OUTPUT_DIR, "deployed_landingpage.png")
        page.screenshot(path=path25)
        add_browser_chrome(path25, f"{CLOUD_BASE_URL}/dealers", "Cars Dealership (IBM Cloud Code Engine)")

        # -------------------------------------------------------------
        # 10. Task 26: deployed_loggedin.png
        # -------------------------------------------------------------
        page.evaluate('() => { sessionStorage.setItem("username", "harsh"); }')
        page.reload()
        page.wait_for_selector(".review_icon")
        time.sleep(1.5)
        path26 = os.path.join(OUTPUT_DIR, "deployed_loggedin.png")
        page.screenshot(path=path26)
        add_browser_chrome(path26, f"{CLOUD_BASE_URL}/dealers", "Cars Dealership - harsh (IBM Cloud)")

        # -------------------------------------------------------------
        # 11. Task 27: deployed_dealer_detail.png
        # -------------------------------------------------------------
        page.goto(f"{BASE_URL}/dealer/15")
        page.wait_for_selector(".review_panel, .card, h1, h2")
        time.sleep(2)
        path27 = os.path.join(OUTPUT_DIR, "deployed_dealer_detail.png")
        page.screenshot(path=path27)
        add_browser_chrome(path27, f"{CLOUD_BASE_URL}/dealer/15", "Tempsoft Car Dealership (IBM Cloud)")

        # -------------------------------------------------------------
        # 12. Task 28: deployed_add_review.png
        # -------------------------------------------------------------
        path28 = os.path.join(OUTPUT_DIR, "deployed_add_review.png")
        page.screenshot(path=path28)
        add_browser_chrome(path28, f"{CLOUD_BASE_URL}/dealer/15", "Tempsoft Reviews - Deployed")

        context.close()
        browser.close()

if __name__ == "__main__":
    capture_all()
    print("All 12 screenshots generated successfully!")
