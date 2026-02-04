import streamlit as st
from streamlit_server_state import server_state, server_state_lock

st.set_page_config(page_title="The Bestie Trio Lab", page_icon="🕵️‍♀️")

st.title("🕵️‍♀️ The Bestie Trio Lab")
st.write("Now supporting 3 friends! Compare your scores across the squad.")

# 1. Shared Chalkboard
if "shared_scores" not in server_state:
    with server_state_lock["shared_scores"]:
        server_state["shared_scores"] = {}

# 2. Indicators (The Traits)
traits = [
    "Matchmaking (Shipping people)", 
    "Crush Speculation", 
    "Imagining Weddings", 
    "Story-Spinning",
    "Easygoing", "Funny", "Mischievous", "Dependable", 
    "Gaming", "Artsy", "Sporty", "Reading"
]

# 3. User Selection - Now with Friend 3!
player_choice = st.radio("Who are you?", ["Friend 1", "Friend 2", "Friend 3"])
name = st.text_input("Enter your nickname:", key="name_input")

st.subheader("Rate your interests (0-10):")
my_results = []
for t in traits:
    val = st.slider(f"{t}", 0, 10, 5, key=f"quiz_{t}_{player_choice}")
    my_results.append(val)

# 4. Save to Cloud
if st.button("Submit to the Cloud ☁️"):
    with server_state_lock["shared_scores"]:
        server_state["shared_scores"][player_choice] = {"name": name, "scores": my_results}
    st.success(f"Scores for {name} saved! Tell the rest of the squad to join.")

st.divider()

# 5. The Triple Reveal
if st.button("🔍 Check Squad Compatibility!"):
    all_data = server_state["shared_scores"]
    
    # We check if at least 2 people have joined to show anything
    if len(all_data) >= 2:
        st.balloons()
        st.header("Squad Results")
        
        # This part looks at everyone who has submitted
        names = [data["name"] for data in all_data.values()]
        st.write(f"Comparing: **{', '.join(names)}**")
        
        # Comparison Logic for 3 people:
        # We calculate the "Average Squad Score" by comparing all pairs
        total_match = 0
        pairs = 0
        
        # We use a nested loop to compare everyone to everyone else
        keys = list(all_data.keys())
        for i in range(len(keys)):
            for j in range(i + 1, len(keys)):
                f1 = all_data[keys[i]]
                f2 = all_data[keys[j]]
                
                diff_sum = sum(abs(f1["scores"][k] - f2["scores"][k]) for k in range(len(traits)))
                max_diff = len(traits) * 10
                match_pct = ((max_diff - diff_sum) / max_diff) * 100
                
                st.write(f"✨ {f1['name']} & {f2['name']}: **{match_pct:.1f}%**")
                total_match += match_pct
                pairs += 1
        
        if pairs > 1:
            avg_squad = total_match / pairs
            st.metric(label="Overall Squad Harmony", value=f"{avg_squad:.1f}%")
    else:
        st.warning("We need at least 2 people to compare! Tell your friends to hit 'Submit'.")
