import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/query"

st.set_page_config(
    page_title="Multimodal Recipe Bot",
    page_icon="🍽️",
    layout="wide"   # 🔥 important for side layout
)

# =======================
# SIDEBAR (FILTERS)
# =======================
st.sidebar.title("🔍 Filters")



cuisine = st.sidebar.selectbox(
    "Cuisine",
    ["Any", "Indian", "North Indian", "South Indian", "Continental", "Chinese"]
)

max_time = st.sidebar.slider(
    "Max Cooking Time (minutes)",
    min_value=10,
    max_value=120,
    step=5,
    value=30
)

veg_only = st.sidebar.checkbox("Vegetarian only")

st.sidebar.markdown("---")
st.sidebar.caption("Filters help refine recipe suggestions")

# =======================
# MAIN CONTENT
# =======================
st.title("🍽️ Multimodal Recipe BOt")
st.write("Ask for recipes based on your preferences or upload a food image")

query = st.text_input(
    "What would you like to cook?",
    placeholder="e.g. Quick Indian dinner under 30 minutes"
)

uploaded_image = st.file_uploader(
    "📸 Upload an image of a dish (optional)",
    type=["jpg", "jpeg", "png"]
)

if uploaded_image:
    st.image(uploaded_image, caption="Uploaded image", width=300)

# =======================
# ACTION
# =======================
if st.button("Get Recipes"):
    with st.spinner("Thinking... 🍳"):

        final_query = query

        # 🔥 IF IMAGE IS UPLOADED → CALL VISION API
        if uploaded_image is not None:
            files = {
                "file": uploaded_image.getvalue()
            }

            vision_response = requests.post(
                "http://127.0.0.1:8000/vision",
                files={"file": uploaded_image}
            )

            if vision_response.status_code == 200:
                image_description = vision_response.json()["description"]
                st.info(f"🖼️ Detected from image: {image_description}")

                # 🔥 USE IMAGE DESCRIPTION AS QUERY
                final_query = image_description
            else:
                st.error("Vision model failed")
                st.stop()

        # 🔥 NOW CALL RAG QUERY
        payload = {
            "query": final_query,
            "cuisine": cuisine,
            "max_time": max_time,
            "veg_only": veg_only,
            
        }

        response = requests.post(API_URL, json=payload)

        if response.status_code == 200:
            st.markdown("## 🍽️ Recipe Suggestions")
            st.write(response.json()["answer"])
        else:
            st.error("Something went wrong")
