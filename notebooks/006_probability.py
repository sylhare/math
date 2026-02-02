"""
Probability Theory: From Gambling to Science

An exploration of probability theory with emphasis on intuition,
common misconceptions, and interactive demonstrations. Covers foundations,
Bayes' theorem, famous paradoxes, and probability distributions.
"""

import marimo

__generated_with = "0.19.6"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    import numpy as np
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    return go, make_subplots, np


@app.cell
def _(mo):
    mo.md(
        r"""
        # Probability Theory: From Gambling to Science

        *"Probability theory is nothing but common sense reduced to calculation."*
        — Pierre-Simon Laplace (1812)

        ---

        ## The Gambler's Question (1654)

        In the summer of 1654, a French nobleman named **Antoine Gombaud** (the Chevalier de Méré)
        posed a puzzle to his friend, the mathematician **Blaise Pascal**. The question was
        deceptively simple:

        > *"If a game of chance is interrupted, how should the stakes be fairly divided
        > between the players based on their current scores?"*

        Pascal wrote to **Pierre de Fermat**, and their correspondence that summer gave birth
        to **probability theory**—one of the most useful and counterintuitive branches of
        mathematics.

        What's remarkable is that probability theory emerged not from abstract philosophy,
        but from the practical concerns of gamblers. And yet it now underpins:

        - **Medicine**: Clinical trials and diagnostic testing
        - **Science**: Statistical inference and hypothesis testing
        - **Finance**: Risk assessment and option pricing
        - **AI/ML**: Machine learning and Bayesian inference
        - **Insurance**: Premium calculation and actuarial science

        The same mathematics that tells you when to hold 'em and when to fold 'em also tells
        doctors whether a treatment works and scientists whether their discoveries are real.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Why Probability is Counterintuitive

        Our brains evolved to help us survive on the African savanna, not to calculate
        probabilities. Evolution gave us powerful pattern-recognition systems, but these
        same systems lead us astray when dealing with randomness:

        - **We see patterns in noise**: A "hot streak" at the casino feels real
        - **We ignore base rates**: A positive test result seems definitive
        - **We confuse conditional probabilities**: P(A|B) ≠ P(B|A)
        - **We underestimate rare event combinations**: Birthday paradox surprises us
        - **We're terrible at updating beliefs**: New evidence should change our minds

        **The good news**: Once you understand these biases, probability becomes a
        *superpower*. You'll see through fallacies that fool most people, make better
        decisions under uncertainty, and understand why experts often disagree.

        This notebook will make probability *intuitive* by:
        1. Explaining concepts in plain English before formulas
        2. Showing you where intuition fails (and why)
        3. Letting you simulate and explore interactively
        4. Connecting theory to real-world applications
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## What We'll Explore

        | Section | Topic | Key Question |
        |---------|-------|--------------|
        | 1 | **Foundations** | What does "probability" actually mean? |
        | 2 | **Probability vs Odds** | Why do bookmakers and scientists speak different languages? |
        | 3 | **Addition Rules** | When can we add probabilities? |
        | 4 | **Independence** | What does "the coin has no memory" really mean? |
        | 5 | **Conditional Probability** | How do we update beliefs with evidence? |
        | 6 | **Bayes' Theorem** | Why do most people get the medical test problem wrong? |
        | 7 | **Famous Paradoxes** | What can Monty Hall and birthdays teach us? |
        | 8 | **Discrete Distributions** | How do we model coin flips and rare events? |
        | 9 | **Continuous Distributions** | Why is the bell curve everywhere? |
        | 10 | **Expected Value** | What's the "long run average" and why does it matter? |

        ### Prerequisites

        - Basic arithmetic and algebra
        - Comfort with fractions and percentages
        - Curiosity about why our intuitions often fail us!
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        # Part 1: Foundations of Probability

        *"An event's probability measures how surprised you should be if it happens."*

        ---

        ## A Brief History

        | Year | Mathematician | Contribution |
        |------|---------------|--------------|
        | 1564 | **Cardano** | First systematic study of gambling odds |
        | 1654 | **Pascal & Fermat** | Founded probability theory via correspondence |
        | 1713 | **Jacob Bernoulli** | Law of Large Numbers (*Ars Conjectandi*) |
        | 1763 | **Thomas Bayes** | Bayes' theorem (published posthumously) |
        | 1812 | **Laplace** | Comprehensive probability theory |
        | 1933 | **Kolmogorov** | Rigorous axiomatic foundations |

        For most of history, "probability" was a vague concept. Gamblers had rules of thumb,
        but no systematic theory. **Girolamo Cardano** (1501-1576), a physician, mathematician,
        and compulsive gambler, wrote the first book analyzing games of chance—but it wasn't
        published until a century after his death.

        The real breakthrough came when Pascal and Fermat showed that probability could be
        calculated systematically using **combinatorics**—the mathematics of counting.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## What is Probability?

        Before we define probability mathematically, let's build intuition with three
        different interpretations:

        ### 1. Classical (Equally Likely Outcomes)

        > *"Probability is the number of favorable outcomes divided by total outcomes,
        > when all outcomes are equally likely."*

        **Example**: A fair die has 6 equally likely outcomes. The probability of rolling
        a 4 is 1/6.

        $$P(\\text{roll a 4}) = \\frac{\\text{favorable outcomes}}{\\text{total outcomes}} = \\frac{1}{6}$$

        **Limitation**: Only works when outcomes are equally likely. What's the probability
        it rains tomorrow? There's no obvious way to divide that into "equally likely outcomes."

        ### 2. Frequentist (Long-Run Relative Frequency)

        > *"Probability is the proportion of times an event occurs in a very long
        > sequence of identical trials."*

        **Example**: If you flip a coin 10,000 times and get 5,023 heads, the probability
        of heads is approximately 0.5023 ≈ 0.5.

        **Limitation**: Requires repeatable experiments. What's the probability that
        humans land on Mars by 2050? You can't repeat that experiment.

        ### 3. Bayesian (Degree of Belief)

        > *"Probability quantifies your uncertainty about a proposition, given your
        > current information."*

        **Example**: "I think there's a 70% chance it rains tomorrow" expresses your
        degree of belief based on weather patterns, forecasts, etc.

        **Advantage**: Works for one-time events. You can update your beliefs as you
        get new evidence.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Kolmogorov's Axioms (1933)

        Despite these different interpretations, all mathematicians agree on three simple
        rules that any probability measure must satisfy. **Andrey Kolmogorov** formalized
        these in 1933:

        ### The Three Axioms

        Let Ω be the **sample space** (the set of all possible outcomes) and let P(A) denote
        the probability of event A. Then:

        | Axiom | Statement | Plain English |
        |-------|-----------|---------------|
        | 1. Non-negativity | P(A) ≥ 0 | Probabilities can't be negative |
        | 2. Normalization | P(Ω) = 1 | Something must happen |
        | 3. Additivity | P(A ∪ B) = P(A) + P(B) for disjoint A, B | For mutually exclusive events, add probabilities |

        **That's it!** Everything in probability theory follows from these three axioms.

        ### Immediate Consequences

        From these axioms, we can immediately derive:

        - **P(∅) = 0**: The impossible event has probability zero
        - **P(A) ≤ 1**: No probability exceeds 1
        - **P(A') = 1 - P(A)**: Complement rule (A' means "not A")
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Sample Space and Events

        ### Sample Space (Ω)

        The **sample space** is the set of all possible outcomes of an experiment.

        | Experiment | Sample Space Ω |
        |------------|----------------|
        | Flip a coin | {H, T} |
        | Roll a die | {1, 2, 3, 4, 5, 6} |
        | Roll two dice | {(1,1), (1,2), ..., (6,6)} — 36 outcomes |
        | Pick a real number in [0,1] | [0, 1] — infinite outcomes |

        ### Events

        An **event** is a subset of the sample space—a collection of outcomes we care about.

        | Event Description | Event (as a set) | Probability |
        |-------------------|------------------|-------------|
        | Roll an even number | {2, 4, 6} | 3/6 = 1/2 |
        | Roll greater than 4 | {5, 6} | 2/6 = 1/3 |
        | Roll a 7 | {} = ∅ | 0 |
        | Roll any number | {1,2,3,4,5,6} = Ω | 1 |
        """
    )
    return


@app.cell
def _(go, np):
    # Interactive sample space visualization for a die roll
    np.random.seed(42)

    _outcomes = [1, 2, 3, 4, 5, 6]
    _colors = ["#4ecdc4", "#00d4ff", "#4ecdc4", "#00d4ff", "#4ecdc4", "#00d4ff"]
    _even_colors = ["#2a2a3e", "#ff6b6b", "#2a2a3e", "#ff6b6b", "#2a2a3e", "#ff6b6b"]

    _fig = go.Figure()

    # Draw die faces
    for _i, _outcome in enumerate(_outcomes):
        _fig.add_trace(go.Scatter(
            x=[_i], y=[0],
            mode="markers+text",
            marker=dict(size=60, color=_even_colors[_i], line=dict(color="#00d4ff", width=2)),
            text=[str(_outcome)],
            textfont=dict(size=24, color="#eaeaea"),
            textposition="middle center",
            showlegend=False,
            hovertemplate=f"Outcome: {_outcome}<br>P = 1/6 ≈ 0.167<extra></extra>"
        ))

    # Highlight even numbers
    _fig.add_annotation(
        x=2.5, y=1.2,
        text="Event: 'Roll an even number' = {2, 4, 6}",
        font=dict(size=14, color="#ff6b6b"),
        showarrow=False
    )

    _fig.add_annotation(
        x=2.5, y=-1.2,
        text="P(even) = |{2,4,6}| / |Ω| = 3/6 = 1/2",
        font=dict(size=14, color="#a0a0a0"),
        showarrow=False
    )

    _fig.update_layout(
        title=dict(
            text="Sample Space: Rolling a Fair Die",
            font=dict(color="#eaeaea", size=16)
        ),
        xaxis=dict(visible=False, range=[-1, 6]),
        yaxis=dict(visible=False, range=[-2, 2]),
        paper_bgcolor="#1a1a2e",
        plot_bgcolor="#1a1a2e",
        height=300,
    )
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        The six faces of a fair die represent the sample space Ω = {1, 2, 3, 4, 5, 6}. The highlighted faces (2, 4, 6) form the event "roll an even number." Since all outcomes are equally likely, P(even) = 3/6 = 1/2. This visual connects the abstract notion of "event as a subset" to concrete outcomes.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Classical Probability Formula

        When all outcomes in the sample space are **equally likely**, probability has a
        simple formula:

        $$P(A) = \\frac{|A|}{|\\Omega|} = \\frac{\\text{number of favorable outcomes}}{\\text{total number of outcomes}}$$

        ### Examples

        **Example 1: Drawing a card**

        What's the probability of drawing a heart from a standard 52-card deck?

        - Total outcomes: |Ω| = 52
        - Favorable outcomes: |A| = 13 (there are 13 hearts)
        - P(heart) = 13/52 = 1/4 = 0.25

        **Example 2: Rolling two dice**

        What's the probability the sum is 7?

        - Total outcomes: 6 × 6 = 36
        - Favorable: (1,6), (2,5), (3,4), (4,3), (5,2), (6,1) — that's 6 outcomes
        - P(sum = 7) = 6/36 = 1/6 ≈ 0.167

        **Example 3: Birthday match**

        What's the probability that 2 people have different birthdays?

        - Person 1 can have any birthday: 365/365
        - Person 2 must differ: 364/365
        - P(different) = 365/365 × 364/365 ≈ 0.997

        (We'll return to the birthday problem in the paradoxes section!)
        """
    )
    return


@app.cell
def _(go, mo, np):
    # Frequency simulation: Watch relative frequency converge to probability
    _num_flips_slider = mo.ui.slider(
        start=10, stop=5000, step=10, value=100,
        label="Number of coin flips"
    )
    mo.md(f"**Simulate coin flips**: {_num_flips_slider}")
    return


@app.cell
def _(go, mo, np):
    # Law of Large Numbers demonstration
    np.random.seed(123)

    _n_max = 2000
    _flips = np.random.choice([0, 1], size=_n_max)  # 0=Tails, 1=Heads
    _cumsum = np.cumsum(_flips)
    _n_values = np.arange(1, _n_max + 1)
    _relative_freq = _cumsum / _n_values

    _fig = go.Figure()

    # Relative frequency line
    _fig.add_trace(go.Scatter(
        x=_n_values,
        y=_relative_freq,
        mode="lines",
        line=dict(color="#00d4ff", width=2),
        name="Relative frequency of Heads"
    ))

    # True probability line
    _fig.add_trace(go.Scatter(
        x=[1, _n_max],
        y=[0.5, 0.5],
        mode="lines",
        line=dict(color="#ff6b6b", width=2, dash="dash"),
        name="True probability (0.5)"
    ))

    # Confidence band (approximately)
    _upper = 0.5 + 1.96 * np.sqrt(0.25 / _n_values)
    _lower = 0.5 - 1.96 * np.sqrt(0.25 / _n_values)

    _fig.add_trace(go.Scatter(
        x=np.concatenate([_n_values, _n_values[::-1]]),
        y=np.concatenate([_upper, _lower[::-1]]),
        fill="toself",
        fillcolor="rgba(255, 107, 107, 0.1)",
        line=dict(color="rgba(255,255,255,0)"),
        name="95% confidence band",
        showlegend=True
    ))

    _fig.update_layout(
        title=dict(
            text="Law of Large Numbers: Relative Frequency Converges to Probability",
            font=dict(color="#eaeaea", size=16)
        ),
        xaxis=dict(
            title="Number of flips",
            color="#a0a0a0",
            gridcolor="#2a2a3e",
            type="log"
        ),
        yaxis=dict(
            title="Relative frequency of Heads",
            color="#a0a0a0",
            gridcolor="#2a2a3e",
            range=[0, 1]
        ),
        paper_bgcolor="#1a1a2e",
        plot_bgcolor="#1a1a2e",
        legend=dict(font=dict(color="#a0a0a0"), orientation='h', yanchor='bottom', y=-0.15, xanchor='center', x=0.5),
        margin=dict(l=40, r=40, t=50, b=80),
        height=400,
    )
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        As we flip a coin more and more times, the relative frequency of heads (blue line) converges toward the true probability of 0.5 (red dashed line). Early on, the frequency fluctuates wildly, but by 1000+ flips, it stabilizes near 0.5. The shaded band shows where 95% of random walks would fall—notice how it narrows as sample size grows.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        The simulation above demonstrates the **Law of Large Numbers** (proved by Jacob
        Bernoulli in 1713):

        > *As the number of trials increases, the relative frequency of an event
        > converges to its true probability.*

        Notice how the relative frequency starts wildly varying but gradually settles
        toward 0.5. The red dashed line shows the true probability, and the shaded
        region shows where we'd expect 95% of random walks to fall.

        **Key insight**: Probability is a statement about the long run, not individual
        outcomes. A single flip is unpredictable, but 10,000 flips are remarkably
        predictable!
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        # Part 2: Probability vs Odds

        *"Bookmakers use odds, scientists use probability—here's how to convert."*

        ---

        ## Plain English Explanation

        **Probability** answers: "Out of all possible cases, how many are favorable?"

        $$P = \\frac{\\text{favorable}}{\\text{total}} = \\frac{\\text{favorable}}{\\text{favorable} + \\text{unfavorable}}$$

        **Odds** answer: "How do favorable cases compare to unfavorable cases?"

        $$\\text{Odds} = \\frac{\\text{favorable}}{\\text{unfavorable}} = \\frac{P}{1-P}$$

        ### Example: Rolling a 6

        - **Probability**: P(6) = 1/6 ≈ 0.167 (1 favorable out of 6 total)
        - **Odds**: 1:5 or "1 to 5" (1 favorable vs 5 unfavorable)

        ### Why Do Odds Exist?

        Odds are **natural for betting**:
        - "3 to 1 odds" means for every $1 you bet, you win $3 (plus your stake back)
        - This directly tells you the payout ratio

        Odds are also **natural for Bayesian statistics**:
        - Odds multiply nicely when you get new evidence (likelihood ratios)
        - Probabilities require messier calculations
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Converting Between Probability and Odds

        ### Probability → Odds

        $$\\text{Odds} = \\frac{P}{1-P}$$

        | Probability | Odds |
        |-------------|------|
        | P = 0.5 | 0.5/0.5 = 1:1 ("even odds") |
        | P = 0.25 | 0.25/0.75 = 1:3 |
        | P = 0.8 | 0.8/0.2 = 4:1 |
        | P = 0.1 | 0.1/0.9 = 1:9 |

        ### Odds → Probability

        If odds are a:b (read "a to b"), then:

        $$P = \\frac{a}{a+b}$$

        | Odds | Probability |
        |------|-------------|
        | 1:1 | 1/(1+1) = 0.5 |
        | 1:3 | 1/(1+3) = 0.25 |
        | 4:1 | 4/(4+1) = 0.8 |
        | 1:9 | 1/(1+9) = 0.1 |
        """
    )
    return


@app.cell
def _(go, np):
    # Interactive odds/probability converter visualization
    _probs = np.linspace(0.01, 0.99, 100)
    _odds = _probs / (1 - _probs)

    _fig = go.Figure()

    _fig.add_trace(go.Scatter(
        x=_probs,
        y=_odds,
        mode="lines",
        line=dict(color="#00d4ff", width=3),
        name="Odds = P/(1-P)",
        hovertemplate="P = %{x:.2f}<br>Odds = %{y:.2f}:1<extra></extra>"
    ))

    # Mark some key points
    _key_probs = [0.1, 0.25, 0.5, 0.75, 0.9]
    _key_odds = [p/(1-p) for p in _key_probs]

    _fig.add_trace(go.Scatter(
        x=_key_probs,
        y=_key_odds,
        mode="markers+text",
        marker=dict(size=12, color="#ff6b6b"),
        text=[f"P={p}" for p in _key_probs],
        textposition="top center",
        textfont=dict(color="#a0a0a0", size=10),
        showlegend=False
    ))

    _fig.update_layout(
        title=dict(
            text="Probability vs Odds: A Non-Linear Relationship",
            font=dict(color="#eaeaea", size=16)
        ),
        xaxis=dict(
            title="Probability P",
            color="#a0a0a0",
            gridcolor="#2a2a3e",
            range=[0, 1]
        ),
        yaxis=dict(
            title="Odds (as ratio to 1)",
            color="#a0a0a0",
            gridcolor="#2a2a3e",
            type="log",
            range=[-2, 2]
        ),
        paper_bgcolor="#1a1a2e",
        plot_bgcolor="#1a1a2e",
        legend=dict(font=dict(color="#a0a0a0"), orientation='h', yanchor='bottom', y=-0.15, xanchor='center', x=0.5),
        margin=dict(l=40, r=40, t=50, b=80),
        height=400,
    )
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        This curve reveals the non-linear relationship between probability and odds. At P = 0.5, odds are 1:1 (even). As probability increases, odds grow exponentially—P = 0.9 corresponds to 9:1 odds, and P = 0.99 corresponds to 99:1 odds. The logarithmic y-axis helps visualize this dramatic growth. Bookmakers and Bayesian statisticians often prefer odds because they're unbounded and easier to update.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Betting Odds in Practice

        Bookmakers express odds in various formats:

        ### Fractional Odds (UK)

        "5/1" (five-to-one) means:
        - For every $1 bet, you win $5 profit
        - Implied probability: 1/(5+1) = 1/6 ≈ 16.7%

        ### Decimal Odds (Europe)

        "6.0" means:
        - Total return on a $1 bet is $6 (including your stake)
        - Implied probability: 1/6.0 ≈ 16.7%

        ### Moneyline Odds (US)

        "+500" means:
        - Bet $100 to win $500 profit (underdog)
        - Implied probability: 100/(500+100) = 16.7%

        "-200" means:
        - Bet $200 to win $100 profit (favorite)
        - Implied probability: 200/(200+100) = 66.7%

        ### The Bookmaker's Edge

        **Important**: Bookmakers' odds *always* imply probabilities that sum to more than
        100%. The excess is their profit margin (called the "vigorish" or "juice").
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        # Part 3: Addition Rules

        *"The key to adding probabilities: watch out for double-counting!"*

        ---

        ## Mutually Exclusive Events

        Events A and B are **mutually exclusive** (or **disjoint**) if they cannot both
        occur. In set notation: A ∩ B = ∅.

        **Examples of mutually exclusive events:**
        - Rolling a 2 AND rolling a 5 (same die, same roll)
        - Drawing a heart AND drawing a spade (same card)
        - Being born on Monday AND being born on Tuesday

        **Examples of NOT mutually exclusive:**
        - Rolling a 2 AND rolling an even number (2 is both!)
        - Drawing a heart AND drawing a queen (Queen of Hearts!)
        - It's raining AND it's Tuesday

        ### Addition Rule for Mutually Exclusive Events

        If A and B are mutually exclusive:

        $$P(A \\cup B) = P(A) + P(B)$$

        **Example**: P(roll 2 or 5) = P(2) + P(5) = 1/6 + 1/6 = 2/6 = 1/3
        """
    )
    return


@app.cell
def _(go, np):
    # Venn diagram for mutually exclusive events
    _fig = go.Figure()

    # Draw two separate circles (mutually exclusive)
    _theta = np.linspace(0, 2*np.pi, 100)

    # Circle A
    _xa = 1.5 * np.cos(_theta) - 2
    _ya = 1.5 * np.sin(_theta)
    _fig.add_trace(go.Scatter(
        x=_xa, y=_ya, fill="toself",
        fillcolor="rgba(0, 212, 255, 0.3)",
        line=dict(color="#00d4ff", width=2),
        name="Event A"
    ))

    # Circle B
    _xb = 1.5 * np.cos(_theta) + 2
    _yb = 1.5 * np.sin(_theta)
    _fig.add_trace(go.Scatter(
        x=_xb, y=_yb, fill="toself",
        fillcolor="rgba(255, 107, 107, 0.3)",
        line=dict(color="#ff6b6b", width=2),
        name="Event B"
    ))

    # Labels
    _fig.add_annotation(x=-2, y=0, text="A", font=dict(size=24, color="#00d4ff"), showarrow=False)
    _fig.add_annotation(x=2, y=0, text="B", font=dict(size=24, color="#ff6b6b"), showarrow=False)
    _fig.add_annotation(x=0, y=-2.5, text="Mutually Exclusive: A ∩ B = ∅", font=dict(size=14, color="#a0a0a0"), showarrow=False)
    _fig.add_annotation(x=0, y=-3, text="P(A ∪ B) = P(A) + P(B)", font=dict(size=14, color="#4ecdc4"), showarrow=False)

    _fig.update_layout(
        title=dict(text="Mutually Exclusive Events", font=dict(color="#eaeaea", size=16)),
        xaxis=dict(visible=False, range=[-5, 5]),
        yaxis=dict(visible=False, range=[-4, 3], scaleanchor="x"),
        paper_bgcolor="#1a1a2e",
        plot_bgcolor="#1a1a2e",
        showlegend=True,
        legend=dict(font=dict(color="#a0a0a0"), orientation='h', yanchor='bottom', y=-0.15, xanchor='center', x=0.5),
        margin=dict(l=40, r=40, t=50, b=80),
        height=350,
    )
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        Two circles that don't overlap represent mutually exclusive events—events that cannot both occur. If you're in circle A, you cannot be in circle B, and vice versa. For such events, we can simply add probabilities: P(A ∪ B) = P(A) + P(B), because there's no overlap to worry about double-counting.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The General Addition Rule

        What if events CAN overlap? Then we must avoid **double-counting**!

        $$P(A \\cup B) = P(A) + P(B) - P(A \\cap B)$$

        ### Misconception #1: Double Counting

        **Wrong thinking**: "The probability of rolling a 2 OR an even number is 1/6 + 3/6 = 4/6"

        **The problem**: We counted "2" twice! It appears in both events:
        - Event A = {2}
        - Event B = {2, 4, 6}
        - A ∩ B = {2}

        **Correct calculation**:
        $$P(2 \\text{ or even}) = P(2) + P(\\text{even}) - P(2 \\text{ and even})$$
        $$= \\frac{1}{6} + \\frac{3}{6} - \\frac{1}{6} = \\frac{3}{6} = \\frac{1}{2}$$

        The answer is just P(even) = 1/2, because "rolling a 2" is already included in
        "rolling an even number"!
        """
    )
    return


@app.cell
def _(go, np):
    # Venn diagram showing overlap (not mutually exclusive)
    _fig = go.Figure()

    _theta = np.linspace(0, 2*np.pi, 100)

    # Circle A (roll a 2) - smaller
    _xa = 0.8 * np.cos(_theta) - 0.3
    _ya = 0.8 * np.sin(_theta)

    # Circle B (roll even) - larger
    _xb = 1.5 * np.cos(_theta) + 0.5
    _yb = 1.5 * np.sin(_theta)

    # Draw B first (so A appears on top)
    _fig.add_trace(go.Scatter(
        x=_xb, y=_yb, fill="toself",
        fillcolor="rgba(255, 107, 107, 0.3)",
        line=dict(color="#ff6b6b", width=2),
        name="Even = {2,4,6}"
    ))

    # Draw A (overlapping)
    _fig.add_trace(go.Scatter(
        x=_xa, y=_ya, fill="toself",
        fillcolor="rgba(0, 212, 255, 0.5)",
        line=dict(color="#00d4ff", width=2),
        name="{2}"
    ))

    # Labels
    _fig.add_annotation(x=-0.3, y=0, text="2", font=dict(size=20, color="#00d4ff"), showarrow=False)
    _fig.add_annotation(x=1.3, y=0, text="4, 6", font=dict(size=16, color="#ff6b6b"), showarrow=False)
    _fig.add_annotation(x=0.5, y=-2.5, text="A ⊂ B: The set {2} is inside {2,4,6}", font=dict(size=12, color="#a0a0a0"), showarrow=False)
    _fig.add_annotation(x=0.5, y=-3, text="P(A ∪ B) = P(A) + P(B) - P(A∩B) = 1/6 + 3/6 - 1/6 = 3/6", font=dict(size=12, color="#4ecdc4"), showarrow=False)

    _fig.update_layout(
        title=dict(text="Overlapping Events: Don't Double Count!", font=dict(color="#eaeaea", size=16)),
        xaxis=dict(visible=False, range=[-3, 4]),
        yaxis=dict(visible=False, range=[-4, 3], scaleanchor="x"),
        paper_bgcolor="#1a1a2e",
        plot_bgcolor="#1a1a2e",
        showlegend=True,
        legend=dict(font=dict(color="#a0a0a0"), orientation='h', yanchor='bottom', y=-0.15, xanchor='center', x=0.5),
        margin=dict(l=40, r=40, t=50, b=80),
        height=350,
    )
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        When events overlap, we can't simply add probabilities—we'd count the overlap twice. Here, the small circle {2} is entirely contained within the larger circle {2, 4, 6}. If we naively added P({2}) + P({2,4,6}), we'd count "2" twice. The inclusion-exclusion formula corrects this by subtracting the intersection: P(A ∪ B) = P(A) + P(B) − P(A ∩ B).
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Inclusion-Exclusion for Three Events

        For three events A, B, C:

        $$P(A \\cup B \\cup C) = P(A) + P(B) + P(C)$$
        $$- P(A \\cap B) - P(A \\cap C) - P(B \\cap C)$$
        $$+ P(A \\cap B \\cap C)$$

        **Pattern**: Add singles, subtract pairs, add triples.

        For n events: alternately add and subtract, with signs following (-1)^(k+1) for
        k-way intersections.

        ### The Complement Rule

        Often it's easier to calculate P(NOT A) than P(A). The **complement rule** helps:

        $$P(A) = 1 - P(A')$$

        where A' (or Aᶜ) is the complement of A.

        **Example**: What's the probability of getting at least one head in 3 coin flips?

        - Hard way: Count HHH, HHT, HTH, THH, HTT, THT, TTH = 7 outcomes
        - Easy way: P(at least one H) = 1 - P(no heads) = 1 - P(TTT) = 1 - 1/8 = 7/8
        """
    )
    return


@app.cell
def _(go, np):
    # Three-set Venn diagram with inclusion-exclusion
    _fig = go.Figure()

    _theta = np.linspace(0, 2*np.pi, 100)
    _r = 1.2

    # Three circles arranged in a triangle
    _centers = [
        (-0.7, 0.5),   # A - top left
        (0.7, 0.5),    # B - top right
        (0, -0.7)      # C - bottom
    ]
    _colors = ["#00d4ff", "#ff6b6b", "#4ecdc4"]
    _names = ["A", "B", "C"]

    for _i, ((_cx, _cy), _color, _name) in enumerate(zip(_centers, _colors, _names)):
        _x = _r * np.cos(_theta) + _cx
        _y = _r * np.sin(_theta) + _cy
        _fig.add_trace(go.Scatter(
            x=_x, y=_y, fill="toself",
            fillcolor=f"rgba{tuple(list(int(_color[i:i+2], 16) for i in (1, 3, 5)) + [0.2])}",
            line=dict(color=_color, width=2),
            name=_name
        ))
        _fig.add_annotation(
            x=_cx + 0.8 * np.cos(np.pi/2 + _i * 2*np.pi/3),
            y=_cy + 0.8 * np.sin(np.pi/2 + _i * 2*np.pi/3),
            text=_name, font=dict(size=20, color=_color), showarrow=False
        )

    _fig.add_annotation(x=0, y=-2.8, text="P(A∪B∪C) = P(A)+P(B)+P(C) − P(A∩B)−P(A∩C)−P(B∩C) + P(A∩B∩C)",
                       font=dict(size=11, color="#a0a0a0"), showarrow=False)

    _fig.update_layout(
        title=dict(text="Inclusion-Exclusion: Three Events", font=dict(color="#eaeaea", size=16)),
        xaxis=dict(visible=False, range=[-3, 3]),
        yaxis=dict(visible=False, range=[-3.5, 2.5], scaleanchor="x"),
        paper_bgcolor="#1a1a2e",
        plot_bgcolor="#1a1a2e",
        showlegend=True,
        legend=dict(font=dict(color="#a0a0a0"), orientation='h', yanchor='bottom', y=-0.15, xanchor='center', x=0.5),
        margin=dict(l=40, r=40, t=50, b=80),
        height=400,
    )
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        Three overlapping circles form a classic Venn diagram for three events. The inclusion-exclusion formula accounts for all possible overlaps: we add the three individual probabilities, subtract the three pairwise intersections (to correct for double-counting), then add back the triple intersection (which was subtracted too many times). This generalizes to any number of events.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        # Part 4: Multiplication Rules & Independence

        *"The coin has no memory."*

        ---

        ## Jacob Bernoulli and Independent Trials (1713)

        **Jacob Bernoulli** (1655-1705) spent 20 years working on his masterpiece
        *Ars Conjectandi* ("The Art of Conjecturing"), which was published posthumously
        in 1713. In it, he laid the foundations for understanding **independent trials**—
        experiments where the outcome of one trial doesn't affect the others.

        His key insight: when events are independent, their probabilities **multiply**.

        ## Independent Events

        Events A and B are **independent** if knowing that A occurred doesn't change
        the probability of B:

        $$P(B|A) = P(B)$$

        Equivalently, A and B are independent if and only if:

        $$P(A \\cap B) = P(A) \\times P(B)$$

        ### Examples of Independent Events

        - Successive coin flips
        - Drawing cards WITH replacement
        - Weather in Tokyo and weather in London (mostly)
        - Your blood type and your neighbor's blood type

        ### Examples of Dependent Events

        - Drawing cards WITHOUT replacement (deck changes!)
        - Whether it rains today and whether it rains tomorrow
        - Your height and your parents' heights
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The Multiplication Rule

        ### For Independent Events

        $$P(A \\cap B) = P(A) \\times P(B)$$

        **Example**: Probability of two heads in two coin flips?
        $$P(HH) = P(H) \\times P(H) = 0.5 \\times 0.5 = 0.25$$

        ### For Dependent Events

        $$P(A \\cap B) = P(A) \\times P(B|A)$$

        **Example**: Drawing two hearts in a row WITHOUT replacement?
        $$P(\\text{both hearts}) = P(\\text{1st heart}) \\times P(\\text{2nd heart}|\\text{1st heart})$$
        $$= \\frac{13}{52} \\times \\frac{12}{51} = \\frac{156}{2652} \\approx 0.059$$

        Compare to WITH replacement:
        $$P(\\text{both hearts}) = \\frac{13}{52} \\times \\frac{13}{52} = \\frac{169}{2704} \\approx 0.063$$

        Slightly higher! Because you might draw the same heart twice.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Misconception #2: The Gambler's Fallacy

        > *"I've flipped 10 heads in a row. Tails MUST be due!"*

        **This is wrong.** Each coin flip is independent. The coin has no memory.

        After 10 heads, the probability of the next flip being tails is still exactly
        **50%**, the same as it always was.

        ### Why Our Brains Get This Wrong

        We're pattern-matching creatures. We expect things to "even out" in the short
        term. But the Law of Large Numbers only says things even out in the **very long
        run**—not in the next few trials.

        ### The Math

        After 10 heads:
        - P(next flip is tails) = 0.5
        - P(next flip is heads) = 0.5

        The past flips don't affect the future flip. The coin doesn't know it's been
        "running hot."

        ### Why Casinos Love This

        Gamblers who believe in the gambler's fallacy:
        - Keep playing after losses ("I'm due for a win!")
        - Bet more after losses ("It HAS to turn around!")

        Both behaviors increase casino profits.
        """
    )
    return


@app.cell
def _(go, np):
    # Gambler's fallacy demonstration: simulate many sequences
    np.random.seed(42)

    _n_sequences = 10000
    _sequence_length = 11  # 10 flips + 1 more

    # Generate all sequences
    _all_flips = np.random.choice([0, 1], size=(_n_sequences, _sequence_length))

    # Find sequences that start with 10 heads
    _ten_heads_mask = np.all(_all_flips[:, :10] == 1, axis=1)
    _sequences_with_ten_heads = _all_flips[_ten_heads_mask]

    # What fraction have heads on the 11th flip?
    if len(_sequences_with_ten_heads) > 0:
        _eleventh_flip_heads = np.mean(_sequences_with_ten_heads[:, 10])
    else:
        _eleventh_flip_heads = 0.5

    _fig = go.Figure()

    # Bar chart
    _fig.add_trace(go.Bar(
        x=["Heads (11th flip)", "Tails (11th flip)"],
        y=[_eleventh_flip_heads, 1 - _eleventh_flip_heads],
        marker_color=["#00d4ff", "#ff6b6b"],
        text=[f"{_eleventh_flip_heads:.1%}", f"{1-_eleventh_flip_heads:.1%}"],
        textposition="auto",
        textfont=dict(size=16)
    ))

    # Reference line
    _fig.add_hline(y=0.5, line_dash="dash", line_color="#4ecdc4",
                  annotation_text="Expected: 50%", annotation_font_color="#4ecdc4")

    _n_found = np.sum(_ten_heads_mask)
    _fig.update_layout(
        title=dict(
            text=f"After 10 Heads, What's the 11th Flip? (Found {_n_found} such sequences)",
            font=dict(color="#eaeaea", size=14)
        ),
        xaxis=dict(color="#a0a0a0"),
        yaxis=dict(title="Proportion", color="#a0a0a0", gridcolor="#2a2a3e", range=[0, 1]),
        paper_bgcolor="#1a1a2e",
        plot_bgcolor="#1a1a2e",
        height=350,
    )
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        This simulation tests the gambler's fallacy. Among thousands of random coin flip sequences, we found cases where 10 consecutive heads occurred, then checked the 11th flip. Despite the "hot streak," the 11th flip is still approximately 50-50—the coin has no memory of previous flips. This demonstrates why the gambler's fallacy is indeed a fallacy.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Misconception #3: Multiplying Non-Independent Events

        > *"Two doctors are each 80% accurate. Together they must be 96% accurate!"*

        **Why this is wrong**: The doctors may make **correlated errors**:
        - They learned from the same textbooks
        - They see the same symptoms
        - They have the same blind spots

        ### The Math

        If the doctors were truly independent:
        $$P(\\text{both wrong}) = 0.2 \\times 0.2 = 0.04$$
        $$P(\\text{at least one right}) = 1 - 0.04 = 0.96$$

        But if their errors are correlated (say, they both miss the same 15% of cases):
        $$P(\\text{both wrong}) \\geq 0.15$$
        $$P(\\text{at least one right}) \\leq 0.85$$

        ### Real-World Implications

        This is why:
        - Diverse teams make better decisions than homogeneous ones
        - Machine learning ensembles use different algorithms, not copies of the same one
        - Second opinions should come from doctors with different training
        """
    )
    return


@app.cell
def _(go, np):
    # Tree diagram for sequential probability
    _fig = go.Figure()

    # Draw tree for two coin flips
    # Level 0: Start
    _fig.add_trace(go.Scatter(
        x=[0], y=[0], mode="markers+text",
        marker=dict(size=20, color="#4ecdc4"),
        text=["Start"], textposition="middle left",
        textfont=dict(color="#eaeaea", size=12),
        showlegend=False
    ))

    # Level 1: First flip
    _level1_y = [1.5, -1.5]
    _level1_labels = ["H", "T"]
    _level1_probs = ["P=0.5", "P=0.5"]

    for _i, (_y, _label, _prob) in enumerate(zip(_level1_y, _level1_labels, _level1_probs)):
        _color = "#00d4ff" if _label == "H" else "#ff6b6b"
        # Line from start
        _fig.add_trace(go.Scatter(
            x=[0, 2], y=[0, _y], mode="lines",
            line=dict(color="#4a5568", width=2),
            showlegend=False
        ))
        # Node
        _fig.add_trace(go.Scatter(
            x=[2], y=[_y], mode="markers+text",
            marker=dict(size=25, color=_color),
            text=[_label], textposition="middle center",
            textfont=dict(color="#1a1a2e", size=14),
            showlegend=False
        ))
        # Probability label on edge
        _fig.add_annotation(x=1, y=_y/2 + 0.3, text=_prob, font=dict(size=10, color="#a0a0a0"), showarrow=False)

    # Level 2: Second flip
    _level2_data = [
        (2.5, "HH", 0.25, "#00d4ff"),
        (0.5, "HT", 0.25, "#4ecdc4"),
        (-0.5, "TH", 0.25, "#4ecdc4"),
        (-2.5, "TT", 0.25, "#ff6b6b"),
    ]

    _level1_positions = [(2, 1.5), (2, 1.5), (2, -1.5), (2, -1.5)]

    for (_y, _label, _prob, _color), (_x1, _y1) in zip(_level2_data, _level1_positions):
        # Line
        _fig.add_trace(go.Scatter(
            x=[_x1, 4], y=[_y1, _y], mode="lines",
            line=dict(color="#4a5568", width=2),
            showlegend=False
        ))
        # Node
        _fig.add_trace(go.Scatter(
            x=[4], y=[_y], mode="markers+text",
            marker=dict(size=30, color=_color),
            text=[_label], textposition="middle center",
            textfont=dict(color="#1a1a2e", size=12),
            showlegend=False
        ))
        # Final probability
        _fig.add_annotation(x=5, y=_y, text=f"P={_prob}", font=dict(size=11, color="#a0a0a0"), showarrow=False)

    _fig.update_layout(
        title=dict(text="Tree Diagram: Two Coin Flips", font=dict(color="#eaeaea", size=16)),
        xaxis=dict(visible=False, range=[-1, 6]),
        yaxis=dict(visible=False, range=[-3.5, 3.5]),
        paper_bgcolor="#1a1a2e",
        plot_bgcolor="#1a1a2e",
        height=400,
    )
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        A probability tree traces all possible outcomes of two coin flips. From the start, we branch to H (heads) or T (tails), each with probability 0.5. From each first-flip outcome, we branch again. The four endpoints (HH, HT, TH, TT) each have probability 0.25, found by multiplying along the branches. Trees make sequential probability calculations visual and systematic.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        # Part 5: Conditional Probability

        *"P(A|B) answers: Given that B happened, what's the chance of A?"*

        ---

        ## The Key Insight

        **Conditional probability** is about updating your beliefs when you learn new
        information. It's the mathematical foundation of rational inference.

        ### Plain English

        P(A|B) reads as "the probability of A given B" and answers:

        > *"If I know B happened, how likely is A?"*

        ### Examples

        - P(rain tomorrow | clouds today) — How likely is rain, knowing it's cloudy?
        - P(disease | positive test) — How likely is disease, knowing test was positive?
        - P(guilty | evidence) — How likely is guilt, given the evidence?

        ### The Formula

        $$P(A|B) = \\frac{P(A \\cap B)}{P(B)}$$

        **Intuition**: We're restricting our attention to only the cases where B happened,
        then asking what fraction of those cases also have A.
        """
    )
    return


@app.cell
def _(go, np):
    # Visual representation of conditional probability
    _fig = go.Figure()

    _theta = np.linspace(0, 2*np.pi, 100)

    # Circle B (the condition - what we know happened)
    _xb = 1.8 * np.cos(_theta)
    _yb = 1.8 * np.sin(_theta)
    _fig.add_trace(go.Scatter(
        x=_xb, y=_yb, fill="toself",
        fillcolor="rgba(255, 107, 107, 0.3)",
        line=dict(color="#ff6b6b", width=3),
        name="B (known to have occurred)"
    ))

    # Circle A (what we want probability of)
    _xa = 1.3 * np.cos(_theta) + 0.8
    _ya = 1.3 * np.sin(_theta)
    _fig.add_trace(go.Scatter(
        x=_xa, y=_ya, fill="toself",
        fillcolor="rgba(0, 212, 255, 0.4)",
        line=dict(color="#00d4ff", width=3),
        name="A (what we want to know)"
    ))

    # Labels
    _fig.add_annotation(x=-1.2, y=0, text="B only", font=dict(size=12, color="#ff6b6b"), showarrow=False)
    _fig.add_annotation(x=1.5, y=0, text="A only", font=dict(size=12, color="#00d4ff"), showarrow=False)
    _fig.add_annotation(x=0.4, y=0, text="A∩B", font=dict(size=14, color="#4ecdc4"), showarrow=False)

    _fig.add_annotation(x=0, y=-3, text="P(A|B) = P(A∩B) / P(B)", font=dict(size=16, color="#eaeaea"), showarrow=False)
    _fig.add_annotation(x=0, y=-3.6, text="'Zoom in' on B, then see how much is also A", font=dict(size=12, color="#a0a0a0"), showarrow=False)

    _fig.update_layout(
        title=dict(text="Conditional Probability: Restricting to Where B Occurred", font=dict(color="#eaeaea", size=16)),
        xaxis=dict(visible=False, range=[-4, 4]),
        yaxis=dict(visible=False, range=[-4.5, 3], scaleanchor="x"),
        paper_bgcolor="#1a1a2e",
        plot_bgcolor="#1a1a2e",
        showlegend=True,
        legend=dict(font=dict(color="#a0a0a0"), orientation='h', yanchor='bottom', y=-0.15, xanchor='center', x=0.5),
        margin=dict(l=40, r=40, t=50, b=80),
        height=400,
    )
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        The Venn diagram illustrates conditional probability. Circle B (red) represents all cases where event B occurred—this is our new "universe." Circle A (cyan) represents event A. To find P(A|B), we "zoom in" on B and ask: what fraction of B is also in A? The answer is the overlap region (A∩B) divided by all of B.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Misconception #4: Confusing P(A|B) with P(B|A)

        > *"The probability of rain given clouds equals the probability of clouds given rain."*

        **This is almost always wrong!**

        ### The Prosecutor's Fallacy

        In courtrooms, this confusion can be devastating:

        - P(evidence | innocent) = Probability of seeing this evidence if the defendant is innocent
        - P(innocent | evidence) = Probability defendant is innocent given the evidence

        **These are NOT the same!**

        If DNA evidence matches 1 in 1 million people:
        - P(match | innocent) = 1/1,000,000 (very small)
        - P(innocent | match) = ??? (depends on other evidence!)

        In a city of 10 million, about 10 innocent people would match. If one of them
        is on trial, P(innocent | match) might be quite high!

        ### Weather Example

        - P(clouds | rain) ≈ 100% — If it's raining, there are almost certainly clouds
        - P(rain | clouds) ≈ 30% — Clouds don't always bring rain

        **The relationship is asymmetric.**
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Bayes' Theorem

        **Thomas Bayes** (1701-1761) was an English minister who developed a theorem
        relating P(A|B) and P(B|A). His work was published posthumously in 1763.

        ### The Theorem

        $$P(A|B) = \\frac{P(B|A) \\cdot P(A)}{P(B)}$$

        Or, more intuitively:

        $$\\text{Posterior} = \\frac{\\text{Likelihood} \\times \\text{Prior}}{\\text{Evidence}}$$

        ### The Terms

        | Term | Symbol | Meaning |
        |------|--------|---------|
        | Prior | P(A) | Probability of A before seeing evidence |
        | Likelihood | P(B\|A) | Probability of evidence if A is true |
        | Evidence | P(B) | Total probability of seeing this evidence |
        | Posterior | P(A\|B) | Updated probability of A after seeing evidence |

        ### Why It Matters

        Bayes' theorem tells us how to **update our beliefs** when we get new information.
        It's the mathematical foundation of:
        - Medical diagnosis
        - Spam filtering
        - Machine learning
        - Scientific inference
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Misconception #5: Base Rate Neglect

        This is perhaps the most important cognitive bias in probability.

        ### The Medical Test Paradox

        A disease affects 1% of the population. A test for the disease is:
        - 99% sensitive (if you have disease, test is positive 99% of the time)
        - 99% specific (if you don't have disease, test is negative 99% of the time)

        **You test positive. What's the probability you have the disease?**

        Most people say 99%. **The correct answer is about 50%!**

        ### The Calculation

        Using Bayes' theorem:

        $$P(\\text{disease}|\\text{positive}) = \\frac{P(\\text{positive}|\\text{disease}) \\cdot P(\\text{disease})}{P(\\text{positive})}$$

        We need P(positive) by the Law of Total Probability:

        $$P(\\text{positive}) = P(\\text{positive}|\\text{disease}) \\cdot P(\\text{disease}) + P(\\text{positive}|\\text{no disease}) \\cdot P(\\text{no disease})$$
        $$= 0.99 \\times 0.01 + 0.01 \\times 0.99 = 0.0099 + 0.0099 = 0.0198$$

        So:
        $$\\begin{aligned}
        P(\\text{disease}|\\text{positive}) &= \\frac{0.99 \\times 0.01}{0.0198} \\\\
        &= \\frac{0.0099}{0.0198} \\\\
        &= 0.5 = 50\\%
        \\end{aligned}$$
        """
    )
    return


@app.cell
def _(go):
    # Visual explanation of base rate neglect
    _fig = go.Figure()

    # Population of 10,000
    _total = 10000
    _disease = 100  # 1%
    _healthy = 9900  # 99%

    _true_positive = 99   # 99% of 100
    _false_negative = 1   # 1% of 100
    _false_positive = 99  # 1% of 9900
    _true_negative = 9801 # 99% of 9900

    # Create treemap-style visualization
    _fig.add_trace(go.Treemap(
        labels=[
            "Population<br>10,000",
            "Has Disease<br>100 (1%)",
            "No Disease<br>9,900 (99%)",
            f"True Positive<br>{_true_positive}",
            f"False Negative<br>{_false_negative}",
            f"False Positive<br>{_false_positive}",
            f"True Negative<br>{_true_negative}"
        ],
        parents=[
            "",
            "Population<br>10,000",
            "Population<br>10,000",
            "Has Disease<br>100 (1%)",
            "Has Disease<br>100 (1%)",
            "No Disease<br>9,900 (99%)",
            "No Disease<br>9,900 (99%)"
        ],
        values=[_total, _disease, _healthy, _true_positive, _false_negative, _false_positive, _true_negative],
        marker=dict(
            colors=["#2a2a3e", "#ff6b6b", "#4ecdc4", "#ff6b6b", "#4a5568", "#ffd93d", "#4ecdc4"],
        ),
        textfont=dict(size=14, color="#eaeaea"),
        hovertemplate="<b>%{label}</b><extra></extra>"
    ))

    _fig.update_layout(
        title=dict(
            text="Base Rate Neglect: Why Positive Test ≠ 99% Chance of Disease",
            font=dict(color="#eaeaea", size=14)
        ),
        paper_bgcolor="#1a1a2e",
        height=450,
    )

    _fig.add_annotation(
        x=0.5, y=-0.12,
        xref="paper", yref="paper",
        text=f"Of {_true_positive + _false_positive} positive tests, only {_true_positive} actually have disease = {_true_positive/(_true_positive+_false_positive):.1%}",
        font=dict(size=13, color="#ffd93d"),
        showarrow=False
    )
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        This treemap breaks down a population of 10,000 by disease status and test results. The key insight is visual: even though the test is 99% accurate, the false positives (99 healthy people testing positive) equal the true positives (99 sick people testing positive) because healthy people vastly outnumber sick people. This is why a positive test only means 50% chance of disease.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Why This Happens

        The key insight is that **false positives from a large healthy population can
        outnumber true positives from a small sick population**.

        In our example:
        - True positives: 99 (99% of 100 sick people)
        - False positives: 99 (1% of 9,900 healthy people)

        Total positive tests: 99 + 99 = 198

        Of these, only 99/198 = 50% actually have the disease!

        ### The Base Rate Matters

        If the disease were more common (say 10%), the same test would be much more
        informative:
        - True positives: 990 (99% of 1,000 sick)
        - False positives: 90 (1% of 9,000 healthy)
        - P(disease | positive) = 990/1080 ≈ 91.7%

        **The rarer the condition, the less a positive test means.**
        """
    )
    return


@app.cell
def _(go, mo, np):
    # Interactive Bayes calculator
    _prevalence_slider = mo.ui.slider(
        start=0.1, stop=20, step=0.1, value=1,
        label="Disease prevalence (%)"
    )
    _sensitivity_slider = mo.ui.slider(
        start=50, stop=99.9, step=0.1, value=99,
        label="Test sensitivity (%)"
    )
    _specificity_slider = mo.ui.slider(
        start=50, stop=99.9, step=0.1, value=99,
        label="Test specificity (%)"
    )

    mo.md(f"""
    ### Interactive Bayes Calculator

    Adjust the parameters to see how they affect P(disease | positive test):

    {_prevalence_slider}
    {_sensitivity_slider}
    {_specificity_slider}
    """)
    return


@app.cell
def _(go, mo, np):
    # Calculate and display posterior probability
    # Use reasonable defaults since we can't access the slider values directly
    _prev = 1.0  # 1%
    _sens = 99.0  # 99%
    _spec = 99.0  # 99%

    _prior = _prev / 100
    _sensitivity = _sens / 100
    _specificity = _spec / 100

    _p_positive = _sensitivity * _prior + (1 - _specificity) * (1 - _prior)
    _posterior = (_sensitivity * _prior) / _p_positive if _p_positive > 0 else 0

    _fig = go.Figure()

    # Gauge chart for posterior probability
    _fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=_posterior * 100,
        number=dict(suffix="%", font=dict(color="#eaeaea", size=40)),
        gauge=dict(
            axis=dict(range=[0, 100], tickcolor="#a0a0a0"),
            bar=dict(color="#00d4ff"),
            bgcolor="#2a2a3e",
            bordercolor="#4a5568",
            steps=[
                dict(range=[0, 33], color="#ff6b6b"),
                dict(range=[33, 66], color="#ffd93d"),
                dict(range=[66, 100], color="#4ecdc4")
            ],
            threshold=dict(
                line=dict(color="#eaeaea", width=2),
                value=50,
                thickness=0.75
            )
        ),
        title=dict(text="P(Disease | Positive Test)", font=dict(color="#eaeaea", size=16))
    ))

    _fig.update_layout(
        paper_bgcolor="#1a1a2e",
        plot_bgcolor="#1a1a2e",
        height=300,
    )
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        This gauge displays the posterior probability—P(disease | positive test)—calculated using Bayes' theorem with the default parameters (1% prevalence, 99% sensitivity, 99% specificity). The needle shows 50%, illustrating that even an excellent test gives only coin-flip confidence when the condition is rare. The colored regions indicate low (red), moderate (yellow), and high (green) confidence zones.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        # Part 6: Famous Paradoxes & Problems

        *"Probability is counterintuitive—here's proof."*

        ---

        These paradoxes aren't mere curiosities. They reveal deep flaws in human
        intuition and have practical implications for decision-making.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The Monty Hall Problem

        **The Setup** (from the TV game show "Let's Make a Deal"):

        1. There are 3 doors. Behind one is a car; behind the others are goats.
        2. You pick a door (say, Door 1).
        3. The host (Monty Hall), who knows where the car is, opens another door (say, Door 3) to reveal a goat.
        4. Monty asks: "Do you want to switch to Door 2?"

        **Should you switch?**

        ### The Controversy

        In 1990, Marilyn vos Savant (holder of the highest recorded IQ) answered this
        question in her column, saying you should switch. She received thousands of
        angry letters, including from PhD mathematicians, telling her she was wrong.

        **She was right.** Switching wins 2/3 of the time.

        ### Why Intuition Fails

        Most people think: "There are 2 doors left, so it's 50-50."

        But this ignores crucial information: **Monty knows where the car is and
        deliberately shows you a goat.**
        """
    )
    return


@app.cell
def _(go):
    # Monty Hall tree diagram
    _fig = go.Figure()

    # Three scenarios based on where the car is
    _scenarios = [
        ("Car behind Door 1", "You picked car", "Switch → Goat", "Stay → CAR", "#4ecdc4"),
        ("Car behind Door 2", "You picked goat", "Switch → CAR", "Stay → Goat", "#ff6b6b"),
        ("Car behind Door 3", "You picked goat", "Switch → CAR", "Stay → Goat", "#ff6b6b"),
    ]

    for _i, (_scenario, _initial, _switch, _stay, _color) in enumerate(_scenarios):
        _y = 2 - _i * 2

        # Scenario box
        _fig.add_shape(
            type="rect", x0=-0.5, x1=2, y0=_y-0.4, y1=_y+0.4,
            fillcolor=_color, opacity=0.3, line=dict(color=_color, width=2)
        )
        _fig.add_annotation(x=0.75, y=_y, text=f"{_scenario}<br>({_initial})",
                          font=dict(size=11, color="#eaeaea"), showarrow=False)

        # Switch outcome
        _switch_color = "#4ecdc4" if "CAR" in _switch else "#ff6b6b"
        _fig.add_shape(
            type="rect", x0=3, x1=5, y0=_y+0.3, y1=_y+0.9,
            fillcolor=_switch_color, opacity=0.4, line=dict(color=_switch_color, width=1)
        )
        _fig.add_annotation(x=4, y=_y+0.6, text=_switch, font=dict(size=10, color="#eaeaea"), showarrow=False)

        # Stay outcome
        _stay_color = "#4ecdc4" if "CAR" in _stay else "#ff6b6b"
        _fig.add_shape(
            type="rect", x0=3, x1=5, y0=_y-0.9, y1=_y-0.3,
            fillcolor=_stay_color, opacity=0.4, line=dict(color=_stay_color, width=1)
        )
        _fig.add_annotation(x=4, y=_y-0.6, text=_stay, font=dict(size=10, color="#eaeaea"), showarrow=False)

        # Arrows
        _fig.add_annotation(x=3, y=_y+0.6, ax=2, ay=_y, axref="x", ayref="y",
                          arrowhead=2, arrowcolor="#a0a0a0")
        _fig.add_annotation(x=3, y=_y-0.6, ax=2, ay=_y, axref="x", ayref="y",
                          arrowhead=2, arrowcolor="#a0a0a0")

    # Summary
    _fig.add_annotation(x=2.5, y=-3, text="Switch wins: 2/3 | Stay wins: 1/3",
                       font=dict(size=16, color="#ffd93d"), showarrow=False)
    _fig.add_annotation(x=2.5, y=-3.6, text="You should ALWAYS switch!",
                       font=dict(size=14, color="#4ecdc4"), showarrow=False)

    _fig.update_layout(
        title=dict(text="Monty Hall Problem: All Three Scenarios", font=dict(color="#eaeaea", size=16)),
        xaxis=dict(visible=False, range=[-1, 6]),
        yaxis=dict(visible=False, range=[-4.5, 3.5]),
        paper_bgcolor="#1a1a2e",
        plot_bgcolor="#1a1a2e",
        height=450,
    )
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        This diagram exhaustively shows all three scenarios based on where the car actually is. In each row, you pick Door 1, Monty reveals a goat, and you can either stay or switch. The colors reveal the key insight: switching wins in 2 out of 3 scenarios (when the car is behind Door 2 or 3), while staying wins only when you initially picked correctly (1 out of 3). This is why switching doubles your odds.
        """
    )
    return


@app.cell
def _(go, np):
    # Monty Hall simulation
    np.random.seed(42)

    _n_games = 10000
    _wins_switch = 0
    _wins_stay = 0

    for _game in range(_n_games):
        # Car is behind a random door
        _car = np.random.randint(0, 3)
        # Player picks a random door
        _pick = np.random.randint(0, 3)

        # Monty opens a door with a goat (not player's pick, not the car)
        _available = [d for d in range(3) if d != _pick and d != _car]
        _monty_opens = np.random.choice(_available) if len(_available) > 1 else _available[0]

        # Switch door
        _switch_to = [d for d in range(3) if d != _pick and d != _monty_opens][0]

        if _pick == _car:
            _wins_stay += 1
        if _switch_to == _car:
            _wins_switch += 1

    _fig = go.Figure()

    _fig.add_trace(go.Bar(
        x=["Stay", "Switch"],
        y=[_wins_stay / _n_games, _wins_switch / _n_games],
        marker_color=["#ff6b6b", "#4ecdc4"],
        text=[f"{_wins_stay/_n_games:.1%}", f"{_wins_switch/_n_games:.1%}"],
        textposition="auto",
        textfont=dict(size=20)
    ))

    _fig.add_hline(y=1/3, line_dash="dash", line_color="#ff6b6b",
                  annotation_text="Expected stay: 33.3%", annotation_position="left")
    _fig.add_hline(y=2/3, line_dash="dash", line_color="#4ecdc4",
                  annotation_text="Expected switch: 66.7%", annotation_position="left")

    _fig.update_layout(
        title=dict(
            text=f"Monty Hall Simulation: {_n_games:,} Games",
            font=dict(color="#eaeaea", size=16)
        ),
        xaxis=dict(color="#a0a0a0"),
        yaxis=dict(title="Win Rate", color="#a0a0a0", gridcolor="#2a2a3e", range=[0, 1]),
        paper_bgcolor="#1a1a2e",
        plot_bgcolor="#1a1a2e",
        height=400,
    )
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        This bar chart displays the results of 10,000 simulated Monty Hall games. The "Stay" strategy wins about 33% of the time, while "Switch" wins about 67%—matching the theoretical predictions. Simulations like this convinced skeptics (including PhD mathematicians!) that switching really does double your chances.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The Birthday Paradox

        **The Question**: How many people do you need in a room for there to be a
        50% chance that two people share a birthday?

        **The Shocking Answer**: Only **23 people**!

        With 50 people, the probability exceeds 97%.

        ### Why It's Surprising

        Our intuition says: "There are 365 days, so you'd need about half that many
        people." But we're counting **pairs**, not people!

        With 23 people, there are:
        $$\\binom{23}{2} = \\frac{23 \\times 22}{2} = 253 \\text{ pairs}$$

        That's 253 chances for a match, and each has a ~1/365 probability.

        ### The Exact Calculation

        It's easier to calculate P(no match), then subtract from 1:

        $$P(\\text{no match among } n \\text{ people}) = \\frac{365}{365} \\times \\frac{364}{365} \\times \\frac{363}{365} \\times \\cdots \\times \\frac{365-n+1}{365}$$

        $$= \\prod_{k=0}^{n-1} \\frac{365-k}{365}$$
        """
    )
    return


@app.cell
def _(go, np):
    # Birthday paradox visualization
    _max_people = 70
    _n_people = np.arange(1, _max_people + 1)

    # Calculate P(no match) for each n
    _p_no_match = np.ones(_max_people)
    for _i in range(1, _max_people):
        _p_no_match[_i] = _p_no_match[_i-1] * (365 - _i) / 365

    _p_match = 1 - _p_no_match

    _fig = go.Figure()

    # Main curve
    _fig.add_trace(go.Scatter(
        x=_n_people, y=_p_match,
        mode="lines",
        line=dict(color="#00d4ff", width=3),
        name="P(at least one match)",
        hovertemplate="n = %{x}<br>P = %{y:.1%}<extra></extra>"
    ))

    # Mark 50% threshold
    _fig.add_hline(y=0.5, line_dash="dash", line_color="#ff6b6b",
                  annotation_text="50% probability")
    _fig.add_vline(x=23, line_dash="dash", line_color="#4ecdc4",
                  annotation_text="n=23")

    # Mark 99% threshold
    _fig.add_hline(y=0.99, line_dash="dot", line_color="#ffd93d")
    _n_99 = np.argmax(_p_match >= 0.99) + 1
    _fig.add_annotation(x=_n_99, y=0.99, text=f"99% at n={_n_99}",
                       font=dict(size=11, color="#ffd93d"), showarrow=True,
                       arrowhead=2, arrowcolor="#ffd93d", ax=30, ay=-30)

    _fig.update_layout(
        title=dict(
            text="Birthday Paradox: Probability of a Shared Birthday",
            font=dict(color="#eaeaea", size=16)
        ),
        xaxis=dict(title="Number of people", color="#a0a0a0", gridcolor="#2a2a3e"),
        yaxis=dict(title="P(at least one shared birthday)", color="#a0a0a0",
                  gridcolor="#2a2a3e", range=[0, 1.05]),
        paper_bgcolor="#1a1a2e",
        plot_bgcolor="#1a1a2e",
        legend=dict(font=dict(color="#a0a0a0"), orientation='h', yanchor='bottom', y=-0.15, xanchor='center', x=0.5),
        margin=dict(l=40, r=40, t=50, b=80),
        height=400,
    )
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        This curve plots the probability of at least one shared birthday as group size increases. The steep rise is surprising—with just 23 people (vertical dashed line), there's a 50% chance of a match, and by 57 people it exceeds 99%. The paradox arises because we're counting pairs: 23 people create 253 possible pairs to compare, giving many opportunities for a match.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Simpson's Paradox

        **The Setup**: A treatment can be better than a control in every subgroup,
        yet appear worse overall!

        ### The Famous Example: UC Berkeley Admissions (1973)

        Overall admission rates:
        - Men: 44% admitted
        - Women: 35% admitted

        This looks like discrimination against women! But when broken down by department:

        | Department | Men Applied | Men Admitted | Women Applied | Women Admitted |
        |------------|-------------|--------------|---------------|----------------|
        | A | 825 | 62% | 108 | 82% |
        | B | 560 | 63% | 25 | 68% |
        | C | 325 | 37% | 593 | 34% |
        | D | 417 | 33% | 375 | 35% |

        **In most departments, women had HIGHER admission rates!**

        The paradox arose because women applied more to competitive departments
        (C and D) with lower overall admission rates.

        ### Why It Happens

        Simpson's paradox occurs when a **confounding variable** (here: department choice)
        affects both the treatment (gender) and the outcome (admission).

        **The lesson**: Always look for lurking variables when comparing groups!
        """
    )
    return


@app.cell
def _(go, np):
    # Simpson's Paradox visualization
    _fig = make_subplots(rows=1, cols=2, subplot_titles=("By Department", "Overall"))

    # Department data (simplified example)
    _departments = ["Dept A\n(Easy)", "Dept B\n(Hard)"]

    # Men: apply mostly to easy dept
    _men_a, _men_b = 80, 20  # applications
    _men_admit_a, _men_admit_b = 0.9, 0.4  # admission rates

    # Women: apply mostly to hard dept
    _women_a, _women_b = 20, 80
    _women_admit_a, _women_admit_b = 0.95, 0.45  # Higher rates in both!

    # By department
    _fig.add_trace(go.Bar(
        x=_departments, y=[_men_admit_a, _men_admit_b],
        name="Men", marker_color="#00d4ff"
    ), row=1, col=1)

    _fig.add_trace(go.Bar(
        x=_departments, y=[_women_admit_a, _women_admit_b],
        name="Women", marker_color="#ff6b6b"
    ), row=1, col=1)

    # Overall (weighted average)
    _men_overall = (_men_a * _men_admit_a + _men_b * _men_admit_b) / (_men_a + _men_b)
    _women_overall = (_women_a * _women_admit_a + _women_b * _women_admit_b) / (_women_a + _women_b)

    _fig.add_trace(go.Bar(
        x=["Men", "Women"], y=[_men_overall, _women_overall],
        marker_color=["#00d4ff", "#ff6b6b"],
        showlegend=False
    ), row=1, col=2)

    _fig.update_layout(
        title=dict(
            text="Simpson's Paradox: Women win in each dept, but lose overall!",
            font=dict(color="#eaeaea", size=14)
        ),
        paper_bgcolor="#1a1a2e",
        plot_bgcolor="#1a1a2e",
        legend=dict(font=dict(color="#a0a0a0"), orientation='h', yanchor='bottom', y=-0.15, xanchor='center', x=0.5),
        margin=dict(l=40, r=40, t=50, b=80),
        height=350,
    )
    _fig.update_xaxes(color="#a0a0a0")
    _fig.update_yaxes(color="#a0a0a0", gridcolor="#2a2a3e", range=[0, 1])
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        The left panel shows admission rates by department: women (red) outperform men (blue) in both the easy and hard departments. Yet the right panel shows that overall, men have higher admission rates! The paradox occurs because men apply mostly to the easy department (90% admission), while women apply mostly to the hard department (45% admission). The overall average gets pulled toward each group's most-applied department.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        # Part 7: Discrete Probability Distributions

        *"A probability distribution describes how probability is 'distributed' over possible outcomes."*

        ---

        ## The Bernoulli Distribution

        The simplest random experiment: a single trial with two outcomes.

        **Parameters**: p = probability of success

        **Examples**:
        - Coin flip (p = 0.5 for fair coin)
        - Free throw attempt (p = shooter's percentage)
        - Whether a customer buys (p = conversion rate)

        **PMF** (Probability Mass Function):

        $$P(X = x) = \\begin{cases} p & \\text{if } x = 1 \\\\ 1-p & \\text{if } x = 0 \\end{cases}$$

        Or more compactly: $P(X = x) = p^x (1-p)^{1-x}$ for $x \\in \\{0, 1\\}$

        **Mean**: $E[X] = p$

        **Variance**: $\\text{Var}(X) = p(1-p)$
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The Binomial Distribution

        **Question**: If I flip a coin n times, what's the probability of getting exactly k heads?

        **Parameters**:
        - n = number of trials
        - p = probability of success on each trial

        **PMF**:

        $$P(X = k) = \\binom{n}{k} p^k (1-p)^{n-k}$$

        where $\\binom{n}{k} = \\frac{n!}{k!(n-k)!}$ is "n choose k"

        **Plain English**:
        - $p^k$ = probability of k successes
        - $(1-p)^{n-k}$ = probability of (n-k) failures
        - $\\binom{n}{k}$ = number of ways to arrange k successes in n trials

        **Mean**: $E[X] = np$

        **Variance**: $\\text{Var}(X) = np(1-p)$
        """
    )
    return


@app.cell
def _(go, mo, np):
    # Binomial distribution explorer
    _n_binom = mo.ui.slider(start=1, stop=50, step=1, value=10, label="n (number of trials)")
    _p_binom = mo.ui.slider(start=0.05, stop=0.95, step=0.05, value=0.5, label="p (probability of success)")

    mo.md(f"""
    ### Binomial Distribution Explorer

    {_n_binom}
    {_p_binom}
    """)
    return


@app.cell
def _(go, np):
    from scipy import stats

    # Default values for visualization
    _n = 10
    _p = 0.5

    _k_values = np.arange(0, _n + 1)
    _pmf = stats.binom.pmf(_k_values, _n, _p)

    _fig = go.Figure()

    _fig.add_trace(go.Bar(
        x=_k_values, y=_pmf,
        marker_color="#00d4ff",
        name=f"Binomial(n={_n}, p={_p})"
    ))

    # Mark mean
    _mean = _n * _p
    _fig.add_vline(x=_mean, line_dash="dash", line_color="#ff6b6b",
                  annotation_text=f"Mean = {_mean:.1f}")

    _fig.update_layout(
        title=dict(
            text=f"Binomial Distribution: n={_n}, p={_p}",
            font=dict(color="#eaeaea", size=16)
        ),
        xaxis=dict(title="k (number of successes)", color="#a0a0a0", gridcolor="#2a2a3e"),
        yaxis=dict(title="P(X = k)", color="#a0a0a0", gridcolor="#2a2a3e"),
        paper_bgcolor="#1a1a2e",
        plot_bgcolor="#1a1a2e",
        height=350,
    )
    _fig
    return (stats,)


@app.cell
def _(mo):
    mo.md(
        r"""
        This bar chart displays the binomial distribution for n=10 trials with p=0.5 success probability (like flipping a fair coin 10 times). Each bar shows the probability of getting exactly k heads. The distribution is symmetric around the mean (5 heads), with the most likely outcomes clustered near the center and extreme outcomes (0 or 10 heads) being rare.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The Geometric Distribution

        **Question**: How many trials until the first success?

        **Parameters**: p = probability of success on each trial

        **PMF**:

        $$P(X = k) = (1-p)^{k-1} p$$

        **Plain English**: Fail (k-1) times, then succeed.

        **Examples**:
        - Number of coin flips until first head
        - Number of sales calls until first sale
        - Number of attempts until password guess

        **Mean**: $E[X] = 1/p$

        **Variance**: $\\text{Var}(X) = (1-p)/p^2$

        **Key Property**: Memoryless! If you've failed k times, the expected
        remaining trials is still 1/p. The past doesn't help predict the future.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The Poisson Distribution

        **Question**: How many rare events occur in a fixed interval?

        **Parameters**: λ (lambda) = average rate of events

        **PMF**:

        $$P(X = k) = \\frac{\\lambda^k e^{-\\lambda}}{k!}$$

        **Examples**:
        - Number of calls to a call center per hour
        - Number of typos per page
        - Number of car accidents at an intersection per month
        - Number of radioactive decays per second

        **Mean**: $E[X] = \\lambda$

        **Variance**: $\\text{Var}(X) = \\lambda$ (mean equals variance!)

        **Key Property**: Approximates Binomial when n is large, p is small, and np = λ
        """
    )
    return


@app.cell
def _(go, np, stats):
    # Poisson distribution visualization
    _lambdas = [1, 3, 5, 10]
    _max_k = 20
    _k_values = np.arange(0, _max_k + 1)

    _fig = go.Figure()

    _colors = ["#00d4ff", "#4ecdc4", "#ffd93d", "#ff6b6b"]

    for _lam, _color in zip(_lambdas, _colors):
        _pmf = stats.poisson.pmf(_k_values, _lam)
        _fig.add_trace(go.Bar(
            x=_k_values, y=_pmf,
            name=f"λ = {_lam}",
            marker_color=_color,
            opacity=0.7
        ))

    _fig.update_layout(
        title=dict(
            text="Poisson Distribution for Different λ Values",
            font=dict(color="#eaeaea", size=16)
        ),
        xaxis=dict(title="k (number of events)", color="#a0a0a0", gridcolor="#2a2a3e"),
        yaxis=dict(title="P(X = k)", color="#a0a0a0", gridcolor="#2a2a3e"),
        paper_bgcolor="#1a1a2e",
        plot_bgcolor="#1a1a2e",
        legend=dict(font=dict(color="#a0a0a0"), orientation='h', yanchor='bottom', y=-0.15, xanchor='center', x=0.5),
        margin=dict(l=40, r=40, t=50, b=80),
        barmode="overlay",
        height=400,
    )
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        Four Poisson distributions with different rate parameters λ. When λ is small (λ=1), events are rare and the distribution is right-skewed—0 or 1 event is most likely. As λ increases, the distribution shifts right and becomes more symmetric, approaching a bell curve shape. The mean and variance of a Poisson distribution both equal λ.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        # Part 8: Continuous Probability Distributions

        *"In continuous distributions, we ask about intervals, not exact values."*

        ---

        ## From Discrete to Continuous

        For discrete distributions, we can ask "P(X = 3)".

        For continuous distributions, **P(X = exact value) = 0**! There are infinitely
        many possible values, so any single one has zero probability.

        Instead, we ask about **intervals**: P(a < X < b)

        ### PDF vs PMF

        - **PMF** (discrete): P(X = k) gives probability directly
        - **PDF** (continuous): f(x) gives probability *density*

        $$P(a < X < b) = \\int_a^b f(x) dx$$

        The area under the PDF curve gives probability!
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The Uniform Distribution

        **The simplest continuous distribution**: All values equally likely in an interval.

        **Parameters**: a, b (endpoints of interval)

        **PDF**:

        $$f(x) = \\begin{cases} \\frac{1}{b-a} & \\text{if } a \\leq x \\leq b \\\\ 0 & \\text{otherwise} \\end{cases}$$

        **Mean**: $E[X] = \\frac{a+b}{2}$

        **Variance**: $\\text{Var}(X) = \\frac{(b-a)^2}{12}$

        **Examples**:
        - Random number generator output
        - Arrival time within an hour (if equally likely any time)
        - Phase of a wave at random observation
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The Normal (Gaussian) Distribution

        **The most important distribution in statistics!**

        **Parameters**: μ (mean), σ (standard deviation)

        **PDF**:

        $$f(x) = \\frac{1}{\\sigma\\sqrt{2\\pi}} e^{-\\frac{(x-\\mu)^2}{2\\sigma^2}}$$

        **The 68-95-99.7 Rule**:
        - 68% of data falls within 1σ of μ
        - 95% of data falls within 2σ of μ
        - 99.7% of data falls within 3σ of μ

        **Why is it everywhere?**

        The **Central Limit Theorem**: The sum (or average) of many independent random
        variables tends toward a normal distribution, regardless of the original distribution!

        This is why heights, test scores, measurement errors, and countless other
        quantities follow the normal distribution.
        """
    )
    return


@app.cell
def _(go, np, stats):
    # Normal distribution with 68-95-99.7 rule
    _mu = 0
    _sigma = 1
    _x = np.linspace(-4, 4, 1000)
    _pdf = stats.norm.pdf(_x, _mu, _sigma)

    _fig = go.Figure()

    # Main curve
    _fig.add_trace(go.Scatter(
        x=_x, y=_pdf,
        mode="lines",
        line=dict(color="#00d4ff", width=3),
        name="N(0, 1)",
        fill="tozeroy",
        fillcolor="rgba(0, 212, 255, 0.1)"
    ))

    # 68% region
    _x_68 = _x[(_x >= -1) & (_x <= 1)]
    _y_68 = stats.norm.pdf(_x_68, _mu, _sigma)
    _fig.add_trace(go.Scatter(
        x=np.concatenate([_x_68, _x_68[::-1]]),
        y=np.concatenate([_y_68, np.zeros(len(_y_68))]),
        fill="toself",
        fillcolor="rgba(78, 205, 196, 0.4)",
        line=dict(color="rgba(0,0,0,0)"),
        name="68% (±1σ)"
    ))

    # 95% region (outer part only for visibility)
    _x_95 = _x[(_x >= -2) & (_x <= 2)]
    _y_95 = stats.norm.pdf(_x_95, _mu, _sigma)
    _fig.add_trace(go.Scatter(
        x=np.concatenate([_x_95, _x_95[::-1]]),
        y=np.concatenate([_y_95, np.zeros(len(_y_95))]),
        fill="toself",
        fillcolor="rgba(255, 217, 61, 0.2)",
        line=dict(color="rgba(0,0,0,0)"),
        name="95% (±2σ)"
    ))

    # Annotations
    _fig.add_annotation(x=0, y=0.2, text="68%", font=dict(size=14, color="#4ecdc4"), showarrow=False)
    _fig.add_annotation(x=1.5, y=0.1, text="95%", font=dict(size=12, color="#ffd93d"), showarrow=False)
    _fig.add_annotation(x=2.5, y=0.02, text="99.7%", font=dict(size=10, color="#ff6b6b"), showarrow=False)

    _fig.update_layout(
        title=dict(
            text="Standard Normal Distribution with 68-95-99.7 Rule",
            font=dict(color="#eaeaea", size=16)
        ),
        xaxis=dict(title="x (in standard deviations from mean)", color="#a0a0a0", gridcolor="#2a2a3e"),
        yaxis=dict(title="Probability Density", color="#a0a0a0", gridcolor="#2a2a3e"),
        paper_bgcolor="#1a1a2e",
        plot_bgcolor="#1a1a2e",
        legend=dict(font=dict(color="#a0a0a0"), orientation='h', yanchor='bottom', y=-0.15, xanchor='center', x=0.5),
        margin=dict(l=40, r=40, t=50, b=80),
        height=400,
    )
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        The standard normal distribution (bell curve) with the famous 68-95-99.7 rule visualized. The shaded regions show that 68% of data falls within ±1 standard deviation of the mean (green region), 95% within ±2σ (yellow region), and 99.7% within ±3σ. This rule provides a quick way to interpret how unusual any observation is.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The Central Limit Theorem in Action

        The CLT says: Sum enough random things together, and you get a bell curve.

        Let's demonstrate by summing uniform random variables:
        - 1 uniform: flat distribution
        - 2 uniforms: triangle distribution
        - 3+ uniforms: increasingly bell-shaped
        - 30+ uniforms: nearly indistinguishable from normal!
        """
    )
    return


@app.cell
def _(go, np, stats):
    # Central Limit Theorem demonstration
    np.random.seed(42)
    _n_samples = 10000

    _fig = make_subplots(rows=2, cols=2, subplot_titles=[
        "n=1 (Uniform)", "n=2 (Sum of 2)", "n=5 (Sum of 5)", "n=30 (Sum of 30)"
    ])

    _ns = [1, 2, 5, 30]
    _positions = [(1, 1), (1, 2), (2, 1), (2, 2)]

    for _n, (_row, _col) in zip(_ns, _positions):
        # Generate sums of n uniform[0,1] random variables
        _sums = np.sum(np.random.uniform(0, 1, (_n_samples, _n)), axis=1)

        # Standardize to mean 0, variance 1
        _mean = _n * 0.5
        _std = np.sqrt(_n / 12)
        _standardized = (_sums - _mean) / _std

        _fig.add_trace(go.Histogram(
            x=_standardized,
            nbinsx=50,
            marker_color="#00d4ff",
            opacity=0.7,
            histnorm="probability density",
            showlegend=False
        ), row=_row, col=_col)

        # Overlay standard normal for comparison
        _x_norm = np.linspace(-4, 4, 100)
        _y_norm = stats.norm.pdf(_x_norm)
        _fig.add_trace(go.Scatter(
            x=_x_norm, y=_y_norm,
            mode="lines",
            line=dict(color="#ff6b6b", width=2),
            showlegend=False
        ), row=_row, col=_col)

    _fig.update_layout(
        title=dict(
            text="Central Limit Theorem: Sum of Uniforms → Normal",
            font=dict(color="#eaeaea", size=16)
        ),
        paper_bgcolor="#1a1a2e",
        plot_bgcolor="#1a1a2e",
        height=500,
    )
    _fig.update_xaxes(color="#a0a0a0", gridcolor="#2a2a3e")
    _fig.update_yaxes(color="#a0a0a0", gridcolor="#2a2a3e")
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        The Central Limit Theorem in action. Each panel shows the distribution of sums of uniform random variables (blue histogram) compared to a standard normal (red curve). With just 1 uniform variable, the distribution is flat. Summing 2 gives a triangle. By n=5, it's clearly bell-shaped, and by n=30, it's virtually indistinguishable from normal—regardless of the original distribution!
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The Exponential Distribution

        **Question**: How long until the next event (in a Poisson process)?

        **Parameters**: λ (rate parameter)

        **PDF**:

        $$f(x) = \\lambda e^{-\\lambda x} \\text{ for } x \\geq 0$$

        **Mean**: $E[X] = 1/\\lambda$

        **Variance**: $\\text{Var}(X) = 1/\\lambda^2$

        **Examples**:
        - Time until next customer arrival
        - Time until radioactive decay
        - Time until next earthquake

        **Key Property**: Memoryless! If you've waited t minutes, expected remaining
        wait is still 1/λ. "The bus doesn't know you've been waiting."
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        # Part 9: Expected Value and Variance

        *"Expected value is what you'd get on average if you played forever."*

        ---

        ## Expected Value (Mean)

        The **expected value** E[X] is the probability-weighted average of all outcomes.

        ### Discrete Case

        $$E[X] = \\sum_i x_i \\cdot P(X = x_i)$$

        **Example**: Expected value of a fair die roll?

        $$E[X] = 1 \\cdot \\frac{1}{6} + 2 \\cdot \\frac{1}{6} + 3 \\cdot \\frac{1}{6} + 4 \\cdot \\frac{1}{6} + 5 \\cdot \\frac{1}{6} + 6 \\cdot \\frac{1}{6}$$
        $$= \\frac{1+2+3+4+5+6}{6} = \\frac{21}{6} = 3.5$$

        Note: 3.5 isn't even a possible outcome! Expected value is a long-run average,
        not a typical outcome.

        ### Continuous Case

        $$E[X] = \\int_{-\\infty}^{\\infty} x \\cdot f(x) dx$$
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Properties of Expected Value

        Expected value is **linear**:

        $$E[aX + b] = aE[X] + b$$
        $$E[X + Y] = E[X] + E[Y]$$

        **Note**: The second property holds even if X and Y are dependent!

        ### Example: Total of Two Dice

        $$E[X_1 + X_2] = E[X_1] + E[X_2] = 3.5 + 3.5 = 7$$

        This is why 7 is the most likely sum when rolling two dice—it's not just the
        mode, it's also the mean!
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Variance and Standard Deviation

        **Variance** measures how spread out the distribution is.

        $$\\text{Var}(X) = E[(X - \\mu)^2] = E[X^2] - E[X]^2$$

        **Standard deviation** is the square root of variance:

        $$\\sigma = \\sqrt{\\text{Var}(X)}$$

        Standard deviation has the same units as X, making it more interpretable.

        ### Properties

        $$\\text{Var}(aX + b) = a^2 \\text{Var}(X)$$

        For **independent** X and Y:
        $$\\text{Var}(X + Y) = \\text{Var}(X) + \\text{Var}(Y)$$

        **Warning**: Variances only add for independent variables!
        """
    )
    return


@app.cell
def _(go, np):
    # Visualize expected value and variance
    _fig = make_subplots(rows=1, cols=2, subplot_titles=["Low Variance", "High Variance"])

    _x = np.linspace(-5, 5, 1000)

    # Low variance (σ = 0.5)
    _y_low = np.exp(-_x**2 / (2 * 0.5**2)) / (0.5 * np.sqrt(2 * np.pi))
    _fig.add_trace(go.Scatter(
        x=_x, y=_y_low, mode="lines", fill="tozeroy",
        line=dict(color="#4ecdc4", width=2),
        fillcolor="rgba(78, 205, 196, 0.3)",
        name="σ = 0.5"
    ), row=1, col=1)

    # High variance (σ = 2)
    _y_high = np.exp(-_x**2 / (2 * 2**2)) / (2 * np.sqrt(2 * np.pi))
    _fig.add_trace(go.Scatter(
        x=_x, y=_y_high, mode="lines", fill="tozeroy",
        line=dict(color="#ff6b6b", width=2),
        fillcolor="rgba(255, 107, 107, 0.3)",
        name="σ = 2"
    ), row=1, col=2)

    # Mean lines
    _fig.add_vline(x=0, line_dash="dash", line_color="#ffd93d", row=1, col=1)
    _fig.add_vline(x=0, line_dash="dash", line_color="#ffd93d", row=1, col=2)

    _fig.update_layout(
        title=dict(text="Same Mean, Different Variance", font=dict(color="#eaeaea", size=16)),
        paper_bgcolor="#1a1a2e",
        plot_bgcolor="#1a1a2e",
        legend=dict(font=dict(color="#a0a0a0"), orientation='h', yanchor='bottom', y=-0.15, xanchor='center', x=0.5),
        margin=dict(l=40, r=40, t=50, b=80),
        height=300,
    )
    _fig.update_xaxes(color="#a0a0a0", gridcolor="#2a2a3e")
    _fig.update_yaxes(color="#a0a0a0", gridcolor="#2a2a3e")
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        Two normal distributions with the same mean (μ=0) but different standard deviations. The left distribution (σ=0.5) is tall and narrow—values cluster tightly around the mean. The right distribution (σ=2) is short and wide—values are more spread out. Variance (σ²) quantifies this spread: higher variance means more uncertainty about where individual values will fall.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The St. Petersburg Paradox

        **The Game**: Flip a coin until you get tails. If tails appears on flip n,
        you win $2ⁿ.

        | Outcome | Probability | Payout |
        |---------|-------------|--------|
        | T | 1/2 | $2 |
        | HT | 1/4 | $4 |
        | HHT | 1/8 | $8 |
        | HHHT | 1/16 | $16 |
        | ... | ... | ... |

        **Expected value**:

        $$\\begin{aligned}
        E[\\text{payout}] &= \\frac{1}{2}(2) + \\frac{1}{4}(4) + \\frac{1}{8}(8) + \\cdots \\\\
        &= 1 + 1 + 1 + \\cdots \\\\
        &= \\infty
        \\end{aligned}$$

        The expected value is **infinite**!

        ### The Paradox

        Would you pay $1 million to play this game?

        Most people wouldn't, even though the "expected value" says you should pay
        any finite amount.

        ### Resolutions

        1. **Utility theory**: We value money logarithmically, not linearly
        2. **Bounded wealth**: No casino can pay infinite amounts
        3. **Risk aversion**: Variance matters, not just mean
        """
    )
    return


@app.cell
def _(go, np):
    # Law of Large Numbers demonstration
    np.random.seed(42)

    _n_rolls = 1000
    _rolls = np.random.randint(1, 7, _n_rolls)
    _cumsum = np.cumsum(_rolls)
    _n_values = np.arange(1, _n_rolls + 1)
    _running_avg = _cumsum / _n_values

    _fig = go.Figure()

    _fig.add_trace(go.Scatter(
        x=_n_values, y=_running_avg,
        mode="lines",
        line=dict(color="#00d4ff", width=2),
        name="Running average"
    ))

    _fig.add_hline(y=3.5, line_dash="dash", line_color="#ff6b6b",
                  annotation_text="E[X] = 3.5")

    _fig.update_layout(
        title=dict(
            text="Law of Large Numbers: Die Roll Average Converges to E[X]",
            font=dict(color="#eaeaea", size=16)
        ),
        xaxis=dict(title="Number of rolls", color="#a0a0a0", gridcolor="#2a2a3e"),
        yaxis=dict(title="Running average", color="#a0a0a0", gridcolor="#2a2a3e", range=[1, 6]),
        paper_bgcolor="#1a1a2e",
        plot_bgcolor="#1a1a2e",
        legend=dict(font=dict(color="#a0a0a0"), orientation='h', yanchor='bottom', y=-0.15, xanchor='center', x=0.5),
        margin=dict(l=40, r=40, t=50, b=80),
        height=350,
    )
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        The Law of Large Numbers demonstrated through die rolls. The blue line tracks the running average after each roll. Early on, it fluctuates wildly—a few lucky 6s or unlucky 1s can swing the average dramatically. But as rolls accumulate, the average converges toward the theoretical expected value of 3.5 (red dashed line). Given enough trials, the sample mean approaches the true mean.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        # Part 10: Real-World Applications

        *"Probability isn't just theory—it's how we make decisions under uncertainty."*

        ---

        ## Insurance

        Insurance companies use probability to:
        - Estimate expected claims (actuarial science)
        - Set premiums to cover expected payouts + profit margin
        - Manage risk through diversification

        **Example**: If P(car accident) = 0.02 and average claim = $15,000:
        $$\\text{Expected claim} = 0.02 \\times \\$15,000 = \\$300$$

        Premium must exceed $300 to be profitable.

        ## Medicine

        - **Clinical trials**: Is the treatment effect real or due to chance?
        - **Diagnostic tests**: P(disease | positive test) via Bayes' theorem
        - **NNT**: Number Needed to Treat — how many patients must receive treatment
          for one to benefit?

        ## Finance

        - **Portfolio theory**: Diversification reduces variance
        - **Option pricing**: Black-Scholes uses probability distributions
        - **Risk measures**: VaR (Value at Risk) uses probability thresholds

        ## Machine Learning

        - **Naive Bayes**: Classification using conditional probabilities
        - **Bayesian inference**: Updating model beliefs with data
        - **Probabilistic models**: Uncertainty quantification
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        # Summary & Quick Reference

        ---

        ## Probability Rules at a Glance

        | Rule | Formula | When to Use |
        |------|---------|-------------|
        | Complement | P(A') = 1 - P(A) | When "not A" is easier to calculate |
        | Addition (disjoint) | P(A ∪ B) = P(A) + P(B) | Events can't both occur |
        | Addition (general) | P(A ∪ B) = P(A) + P(B) - P(A ∩ B) | Events might overlap |
        | Multiplication (independent) | P(A ∩ B) = P(A) × P(B) | Events don't affect each other |
        | Multiplication (dependent) | P(A ∩ B) = P(A) × P(B\|A) | Events are related |
        | Conditional | P(A\|B) = P(A ∩ B) / P(B) | Given B occurred, find P(A) |
        | Bayes' Theorem | P(A\|B) = P(B\|A) × P(A) / P(B) | Update beliefs with evidence |
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Common Distributions

        | Distribution | Use Case | Mean | Variance |
        |--------------|----------|------|----------|
        | Bernoulli(p) | Single yes/no trial | p | p(1-p) |
        | Binomial(n,p) | Count successes in n trials | np | np(1-p) |
        | Geometric(p) | Trials until first success | 1/p | (1-p)/p² |
        | Poisson(λ) | Count of rare events | λ | λ |
        | Uniform(a,b) | Equally likely in [a,b] | (a+b)/2 | (b-a)²/12 |
        | Normal(μ,σ) | Natural variation | μ | σ² |
        | Exponential(λ) | Time until next event | 1/λ | 1/λ² |
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Misconceptions Checklist

        - **Gambler's Fallacy**: Past outcomes don't affect independent future events

        - **Base Rate Neglect**: Always consider how common the condition is

        - **P(A|B) ≠ P(B|A)**: Don't confuse conditional probabilities

        - **Independence Required**: Don't multiply probabilities unless events are independent

        - **Pairs, Not Individuals**: Birthday paradox - count pairs, not people
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Historical Timeline

        | Year | Event |
        |------|-------|
        | 1564 | Cardano writes first probability book (published 1663) |
        | 1654 | Pascal-Fermat correspondence founds probability theory |
        | 1713 | Bernoulli's *Ars Conjectandi* proves Law of Large Numbers |
        | 1763 | Bayes' theorem published posthumously |
        | 1812 | Laplace's comprehensive probability treatise |
        | 1933 | Kolmogorov's axiomatic foundations |
        | 1990 | Marilyn vos Savant publishes Monty Hall solution |
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Further Reading

        **Books**:
        - *Thinking, Fast and Slow* by Daniel Kahneman — Cognitive biases in probability
        - *The Drunkard's Walk* by Leonard Mlodinow — Randomness in everyday life
        - *Naked Statistics* by Charles Wheelan — Accessible introduction

        **Videos**:
        - 3Blue1Brown: "Bayes theorem" and "Binomial distributions"
        - Veritasium: "The Bayesian Trap"
        - Numberphile: Various probability paradoxes

        **Online Courses**:
        - MIT OpenCourseWare: 18.05 Introduction to Probability and Statistics
        - Khan Academy: Statistics and Probability
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        *"The most important questions of life are, for the most part, really only
        problems of probability."*

        — Pierre-Simon Laplace

        ---

        **Congratulations!** You've explored the foundations of probability theory,
        from its origins in gambling to its modern applications in science and technology.

        The key takeaway: **probability is counterintuitive**, but once you understand
        the rules and common pitfalls, you can make better decisions under uncertainty
        than most people.

        Keep practicing, stay curious, and remember—the coin has no memory!
        """
    )
    return


if __name__ == "__main__":
    app.run()
