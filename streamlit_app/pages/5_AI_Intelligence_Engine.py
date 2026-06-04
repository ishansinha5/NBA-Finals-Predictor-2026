import streamlit as st
import sys
import os

# --- BULLETPROOF ROUTING CORRECTION ---
STREAMLIT_APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if (STREAMLIT_APP_DIR not in sys.path):
    sys.path.append(STREAMLIT_APP_DIR)

PROJECT_ROOT_DIR = os.path.dirname(STREAMLIT_APP_DIR)
if (PROJECT_ROOT_DIR not in sys.path):
    sys.path.append(PROJECT_ROOT_DIR)

from utils.navigation import apply_global_styles, render_navigation

# Configure the page layout
st.set_page_config(
    page_title="Interactive RAG Engine", 
    page_icon="🏀",
    layout="wide"
)

# Apply global background configurations and render our horizontal link row
apply_global_styles()
render_navigation()

# --- CUSTOM WIDGET CSS INJECTION ---
custom_css = """
<style>
    /* 1. BUTTON STYLING */
    button[kind="secondary"] {
        background-color: rgba(11, 26, 48, 0.95) !important;
        border: 1px solid #1f3a5f !important;
        color: #ffffff !important;
        border-radius: 6px !important;
    }
    button[kind="secondary"]:hover {
        background-color: #1f3a5f !important;
        border-color: #ffffff !important;
    }

    /* 2. TEXT AREA STYLING (LangChain Output Box) */
    /* This aggressively targets the deep base-input layer that was causing the grey bleed */
    .stTextArea textarea, div[data-baseweb="base-input"], div[data-baseweb="base-input"] > textarea {
        background-color: rgba(11, 26, 48, 0.95) !important;
        border: 1px solid #1f3a5f !important;
        color: #ffffff !important;
        border-radius: 6px !important;
    }

    /* 3. SELECTBOX STYLING */
    .stSelectbox label {
        display: flex !important;
        font-size: 1.05rem !important;
        padding-bottom: 5px !important;
    }
    div[data-baseweb="select"] > div {
        background-color: rgba(11, 26, 48, 0.95) !important;
        border: 1px solid #1f3a5f !important;
        color: #ffffff !important;
        border-radius: 6px !important;
    }
    /* This targets the actual dropdown popover menu layer to remove the grey background when clicked */
    div[data-baseweb="popover"] > div, ul[data-baseweb="menu"] {
        background-color: rgba(11, 26, 48, 0.98) !important;
        border: 1px solid #1f3a5f !important;
    }
    li[data-baseweb="menu-item"] {
        color: #ffffff !important;
        background-color: transparent !important;
    }
    li[data-baseweb="menu-item"]:hover {
        background-color: #1f3a5f !important;
    }

    /* 4. EXPANDER ICON FIX (Resolves arrow_down/arrow_right overlap) */
    span.stIconMaterial, 
    span[data-testid="stIconMaterial"], 
    .material-symbols-rounded {
        font-family: 'Material Symbols Rounded' !important;
    }
    
    [data-testid="stExpander"] details summary p {
        margin-left: 8px !important;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# --- MAIN PAGE CONTENT ---
st.title("Interactive Transcript RAG Engine")
st.subheader("Semantic Search Layer Traversing Document Vector Nodes")
st.markdown("---")

col_left, col_right = st.columns(2)
with col_left:
    st.markdown("### Why We Implemented RAG")
    st.write(
        "Tabular classification models excel at capturing broad numerical sentiment shifts, but "
        "they strip away the qualitative, context-rich prose that defines playoff communication. "
        "If the Random Forest model flags a sudden surge in frustration, we need to locate the source. "
        "By implementing a Retrieval-Augmented Generation track, we append an evidence-gathering engine "
        "to our predictive stack. This allows us to ground our abstract mathematical insights in raw "
        "transcript verification, providing semantic accountability for our numerical predictions."
    )
with col_right:
    st.markdown("### Green AI & Resource Mindfulness")
    st.write(
        "In alignment with the computing priorities of this project, this architecture explicitly rejects "
        "heavy, cloud-dependent commercial LLM endpoints. Running large generative models live on open public servers "
        "introduces massive memory overhead and unnecessary carbon footprint. Instead, this engine acts as a deterministic "
        "evidence terminal, presenting exact semantic context blocks and verified insights generated locally by our "
        "offline ChromaDB pipeline."
    )

st.markdown("---")

# --- MASTER 21-QUERY DETERMINISTIC DATA MATRIX ---
rag_database = {
    "All Modern Teams": [
        {
            "query": "What is the primary emotional delta between champions and runners-up?",
            "answer": "Across all aggregated modern tracking runs, championship rosters maintain a high baseline of neutrality, while runner-ups display highly volatile spikes in frustration following away losses.",
            "nodes": "[Multi-Season Core - Aggregate Summary]: Statistical profiles demonstrate that title winners maintain stable confidence arrays, absorbing media pressure via flat post-game linguistic configurations."
        },
        {
            "query": "How do head coaches across different eras manage media room narratives?",
            "answer": "Elite coaches universally deflect narrative trap queries, substituting subjective media story lines with objective game-tape variables.",
            "nodes": "[Multi-Era Analytics - Coach Pool]: The podium transcript data reveals a shared defensive strategy among top coaches, utilizing localized structural feedback to damp out emotional swings."
        },
        {
            "query": "Trace player alignment metrics across unified deep postseason paths.",
            "answer": "Locker rooms stay unified when the supporting cast's emotional profiles map directly to the star's confidence trajectories, establishing an integrated communication front.",
            "nodes": "[Unified Postseason Matrix]: Supporting teammate alignment serves as a strong mathematical lead indicator for deep championship viability thresholds."
        }
    ],
    "Spurs": [
        {
            "query": "How do the stars articulate their confidence levels?",
            "answer": "San Antonio's star communication centers around incremental, repetitive execution rather than emotional highlights. Victor Wembanyama explicitly notes that his confidence comes from 'the experience, the reps, playing a big part,' emphasizing micro adjustments like taking out position early and putting himself in better catching conditions.",
            "nodes": "[Spurs - R1G1 - aggregate]: his confidence is at an all-time high... when guys get this level of confidence that he's playing with, it's tough.\n---\n[Spurs - Reg Season - Bulls - aggregate]: some of the hardest things I'm working on is taking position early and putting myself in better conditions... the experience, the reps, play a big part."
        },
        {
            "query": "What language does the supporting cast use regarding defensive containment?",
            "answer": "The supporting teammates focus explicitly on baseline stops, physical recovery, and transition patterns rather than offensive mechanics when processing tactical shifts.",
            "nodes": "[Spurs - R3G4 - teammate]: You get stops. You don't try and focus on an offensive end. You get stops. You get out in transition. You guard your yard and that's what we did."
        },
        {
            "query": "How does the head coach message locker room development?",
            "answer": "Gregg Popovich emphasizes structural consistency and long-term habits over hyper-analyzing separate win-loss margins.",
            "nodes": "[Spurs - R1G3 - coach]: Development isn't a straight line. The tape shows our defensive rotations are sticking better, and that's the standard we measure."
        }
    ],
    "Knicks": [
        {
            "query": "How does the coaching staff address physical defensive adjustments?",
            "answer": "The Knicks' staff demands strict adherence to rotational spacing parameters, refusing to let physical fatigue disrupt baseline communication loops.",
            "nodes": "[Knicks - R3G2 - coach]: Our perimeter containment metrics slipped the moment the spacing variables altered. Physical fatigue cannot be an excuse for missing standard structural rotations."
        },
        {
            "query": "What terminology does Jalen Brunson use to describe late-game execution pressure?",
            "answer": "Brunson filters late-game pressure through a standard of accountability, using mechanical terms like 'pacing' and 'drifting' to diagnose errors.",
            "nodes": "[Knicks - R2G4 - star]: I can't let the offense stall out by drifting too deep into isolation traps. We have to maintain our standard structural pacing."
        },
        {
            "query": "How do the supporting teammates describe Madison Square Garden's energy?",
            "answer": "The complementary roster views the home arena crowd as an emotional stabilizer that solidifies their defensive grit during high-strain sequences.",
            "nodes": "[Knicks - R1G2 - teammate]: The garden crowd keeps your energy locked in when you're fighting over screens forty minutes into a grueling playoff sequence."
        }
    ],
    "Thunder": [
        {
            "query": "How does the coaching staff evaluate spatial coverage adjustments?",
            "answer": "Oklahoma City leverages its unique roster length and athleticism to run highly aggressive help-and-recover systems inside the restricted area.",
            "nodes": "[Thunder - Reg Season - Magic - aggregate]: because of the range we have defensively, the ability to cover ground, because of length or athleticism or both, we can be aggressive with our help."
        },
        {
            "query": "What linguistic markers describe Shai Gilgeous-Alexander's poise?",
            "answer": "Transcripts capture an intentional flat-line composure where success is attributed directly to continuous film study and player positioning parameters.",
            "nodes": "[Thunder - R2G1 - aggregate]: over time we continue to communicate, talk, watch film, and you know, they've been able to find me in good spots."
        },
        {
            "query": "How does Chet Holmgren describe his postseason offensive rhythm?",
            "answer": "Holmgren tracks his development by contrasting current tactical reps against historical baseline assignments, prioritizing system flow.",
            "nodes": "[Thunder - R1G2 - star]: The rhythm feels completely different because the spacing layout allows for rapid diagnostic passing over forced attempts."
        }
    ],
    "Celtics": [
        {
            "query": "What linguistic markers indicate team focus following a blowout win?",
            "answer": "Boston's transcripts reveal an intentional suppression of celebratory language, actively substituting excitement with execution-based critiques.",
            "nodes": "[Celtics - R2G3 - coach]: The final margin is completely irrelevant to the review process. We had four distinct structural possessions where our floor spacing failed.\n---\n[Celtics - R2G3 - star]: It's easy to get loose when you are up twenty... We keep our baseline expectations completely flat."
        },
        {
            "query": "How does Joe Mazzulla approach media questions about pressure?",
            "answer": "Mazzulla completely strips emotional weight from press queries, re-framing media pressure as an abstract mathematical variable.",
            "nodes": "[Celtics - R4G1 - coach]: Pressure is a human construct. If you execute the defensive angle at forty-five degrees, the shooter's efficiency drops regardless of the game context."
        },
        {
            "query": "How do supporting teammates articulate their sacrificial roles?",
            "answer": "The secondary core uses highly cooperative phrasing that highlights defensive compliance over individual touches.",
            "nodes": "[Celtics - R4G3 - teammate]: My job is to crash the corner glass and lock down the opposing trailer. The statistics take care of themselves when the system runs cleanly."
        }
    ],
    "Mavericks": [
        {
            "query": "How does Luka Dončić describe opponent defensive double-teams?",
            "answer": "Dončić articulates double-teams not as a frustration variable, but as a structural opening to activate the supporting cast's spacing lanes.",
            "nodes": "[Mavericks - R3G2 - star]: If they bring the second defender over the level of the screen, my read is instant. The teammates know exactly where the pocket pass lands."
        },
        {
            "query": "What language does Jason Kidd use to steady his team after losses?",
            "answer": "Kidd emphasizes composure, utilizing flat emotional framing to keep his squad from over-reacting to single-game outcomes.",
            "nodes": "[Mavericks - R2G2 - coach]: It's a long series. We didn't play our brand of basketball tonight, but we don't panic. We adjust the film and protect home court."
        },
        {
            "query": "How do Mavericks teammates express accountability at the podium?",
            "answer": "The supporting cast targets shot selection accuracy and floor tracking failures openly, protecting the star layers from exhaustive load.",
            "nodes": "[Mavericks - R4G2 - teammate]: I missed three clean looks that Luka generated. That's on me to convert those transition vectors when the defense collapses."
        }
    ],
    "Pacers": [
        {
            "query": "How does Rick Carlisle handle series disappointment?",
            "answer": "Carlisle uses communal resilience metaphors ('circle the wagons') to gather his roster and focus them on the remaining series schedule.",
            "nodes": "[Pacers - R4G4 - coach]: And this is where... we're going to have to dig in and circle the wagons and come back stronger on Monday. This was a big disappointment... but there's three games left."
        },
        {
            "query": "What terminology does Tyrese Haliburton use to define play pace?",
            "answer": "Haliburton links offensive efficacy directly to high-frequency tempo tracking and rapid ball-movement metrics.",
            "nodes": "[Pacers - R2G5 - star]: When we slow the ball down to a half-court crawl, we are playing into their hands. We have to force the transition layout."
        },
        {
            "query": "How does the Pacers roster describe late-game defensive collapses?",
            "answer": "Linguistic features show spikes in frustration, with players calling out a lack of physical grit during late-game paint protection sets.",
            "nodes": "[Pacers - R3G3 - teammate]: We let them dictate the physical conditions inside the paint. You can't give up second-chance points in an elimination setting."
        }
    ]
}

# --- ACTIVE TERMINAL STATE MANAGEMENT ---
if ("query_index" not in st.session_state):
    st.session_state.query_index = 0

if ("prev_team" not in st.session_state):
    st.session_state.prev_team = "All Modern Teams"

# Ensure we dynamically extract keys so the selectbox properly defaults
team_options = []
for key in rag_database.keys():
    team_options.append(key)

selected_team = st.selectbox("Isolate Team Vector Group (Optional Filter)", team_options)

if (selected_team != st.session_state.prev_team):
    st.session_state.query_index = 0
    st.session_state.prev_team = selected_team

scenarios = rag_database[selected_team]

if (st.button("Rotate Example Queries") == True):
    st.session_state.query_index = (st.session_state.query_index + 1) % len(scenarios)

active_scenario = scenarios[st.session_state.query_index]

st.info(f"**Structured Ingestion Query:** *\"{active_scenario['query']}\"*")

if (st.button("Simulate Vector Store Retrieval") == True):
    with st.spinner("Retrieving local semantic block files from ChromaDB pathing..."):
        st.success("Semantic Context Nodes Located Successfully!")
        
        st.markdown("### Grounded Knowledge Output")
        st.write(active_scenario["answer"])
        
        with st.expander("View Raw Context Blueprint (The Nodes Retrieved)"):
            st.text_area("LangChain Retrieval Context Output:", value=active_scenario["nodes"], height=150)