import streamlit as st

# Set up the Page Title and Look
st.set_page_config(page_title="The Bestie Lab", page_icon="🧪")

st.title("🧪 The Bestie Compatibility Lab")
st.write("Find out if you and your friend are a perfect match!")

# Define our specialized categories
social_lab = ["Matchmaking", "Crush Speculation", "Imagining Weddings", "Story-Spinning"]
personality = ["Easygoing", "Funny", "Mischievous", "Dependable"]
hobbies = ["Gaming", "Artsy", "Sporty", "Reading"]
all_traits = social_lab + personality + hobbies

# Create two columns so friends can take it side-by-side
col1, col2 = st.columns(2)

with col1:
    st.header("Friend 1")
    name1 = st.text_input("Name", "User 1")
    scores1 = []
    for trait in all_traits:
        s = st.slider(f"{trait}", 0, 10, 5, key=f"u1_{trait}")
        scores1.append(max(s, 0.1))

with col2:
    st.header("Friend 2")
    name2 = st.text_input("Name", "User 2")
    scores2 = []
    for trait in all_traits:
        s = st.slider(f"{trait}", 0, 10, 5, key=f"u2_{trait}")
        scores2.append(max(s, 0.1))

# The Calculation Button
if st.button("Calculate Our Compatibility! ✨"):
    # Using Absolute Difference logic
    diff_sum = sum(abs(scores1[i] - scores2[i]) for i in range(len(scores1)))
    max_diff = len(all_traits) * 10
    match_pct = ((max_diff - diff_sum) / max_diff) * 100

    st.balloons() # This adds a celebration effect!
    
    st.divider()
    st.subheader(f"Results for {name1} & {name2}")
    st.metric(label="Compatibility Score", value=f"{match_pct:.1f}%")

    if scores1[0] > 7 and scores2[0] > 7:
        st.warning("⚠️ High Matchmaking Energy Detected: No secret is safe with you two!")
    
    if match_pct > 80:
        st.success("You're practically the same person! 👯‍♀️")
    elif match_pct > 50:
        st.info("A solid friendship! Enough in common to never be bored. 🌈")
    else:
        st.write("Opposites attract! You bring different vibes to the table. 🧩")
