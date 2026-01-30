import marimo

__generated_with = "0.9.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import plotly.graph_objects as go
    import sympy as sp
    from sympy import Symbol, sin, cos, exp, log, sqrt
    import polars as pl
    return go, mo, np, pl, sp, cos, exp, log, sin, sqrt, Symbol


@app.cell
def _(mo):
    mo.md(
        r"""
        # Functions and Derivatives
        ## A Journey Through the Birth of Calculus

        *"I do not know what I may appear to the world, but to myself I seem to have been only like a
        boy playing on the seashore, and diverting myself in now and then finding a smoother pebble
        or a prettier shell than ordinary, whilst the great ocean of truth lay all undiscovered before me."*
        — Isaac Newton

        ---

        This notebook explores one of the greatest intellectual achievements in human history:
        the development of calculus. We'll follow the path of Newton and Leibniz as they discovered
        how to describe the mathematics of change.

        **What you'll learn:**
        - Why ancient mathematics couldn't handle motion and change
        - The key insight that makes calculus work: the concept of a **limit**
        - How to compute derivatives using simple rules
        - What derivatives tell us about the shape and behavior of functions
        - Real applications in physics and optimization
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Part I: The Great Problem of the 17th Century

        ### The World Was Moving—But How to Describe It?

        By the 1600s, scientists understood that everything was in motion. Planets orbited the sun.
        Cannonballs traced arcs through the air. Objects fell faster and faster toward the ground.

        But they faced a fundamental problem: **How do you describe changing quantities mathematically?**

        The Greeks had mastered static geometry—circles, triangles, the golden ratio. But their tools
        couldn't handle motion. When a ball rolls down a hill, its speed changes every instant.
        How can you pin down something that never stays the same?

        **The core difficulty**: To calculate speed, you need to divide distance by time. But at a
        single instant:
        - No time passes (time interval = 0)
        - No distance is covered (distance = 0)
        - Speed = 0/0 = ???

        This is the **paradox of instantaneous change**. The Greeks knew about it—Zeno's paradoxes
        explored similar ideas—but they never resolved it. It took nearly two thousand years before
        Newton and Leibniz found the answer.

        This was the problem that consumed the greatest minds of the era: Galileo, Kepler, Fermat,
        and eventually two men whose rivalry would change mathematics forever.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Part II: The Heroes of Our Story

        ### Isaac Newton (1643-1727): The Plague Years

        In 1665, the Great Plague swept through England. Cambridge University closed its doors,
        and a 23-year-old Isaac Newton retreated to his family farm in Woolsthorpe.

        What happened next is one of the most productive periods in scientific history. In just
        two years of isolation, Newton:

        - Developed his theory of **gravity**
        - Discovered that white light contains all colors
        - Invented what he called the **"Method of Fluxions"**—what we now call calculus

        Newton saw quantities as "flowing" through time. A variable wasn't a fixed point; it was
        something that *flowed*. He called these flowing quantities **fluents**, and their rates
        of change **fluxions**.

        His key insight was to think of $h$ (the time interval) not as zero, but as something
        **infinitely small but not zero**—small enough to ignore in some contexts, but not so
        small that you can't divide by it. This was mathematically imprecise, but it worked.

        > 📚 **Primary Source**: [Newton's Method of Fluxions (1671)](https://archive.org/details/methodoffluxions00newt)

        ### Gottfried Wilhelm Leibniz (1646-1716): The Philosopher's Approach

        Meanwhile, in Germany, a diplomat and philosopher named Leibniz was approaching the same
        problem from a completely different angle.

        Where Newton thought of motion and physics, Leibniz thought of infinitely small quantities—
        **infinitesimals**. He imagined dividing a curve into infinitely many infinitely small pieces.

        Leibniz gave us the notation we still use today:
        - **dy/dx** for the derivative (read as "the change in y per change in x")
        - **∫** for the integral (a stylized "S" for "summa", meaning sum)

        His notation suggests the key idea: $\frac{dy}{dx}$ looks like a fraction because it
        *behaves* like one. The "d" stands for an infinitesimally small difference.

        > 📚 **Primary Source**: [Leibniz's Nova Methodus (1684)](https://www.maa.org/press/periodicals/convergence/mathematical-treasure-leibnizs-papers-on-calculus-differential-calculus)
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### The Priority Dispute

        Both Newton and Leibniz independently invented calculus—one of the most remarkable
        coincidences in the history of science. But neither man saw it that way.

        A bitter dispute erupted over who deserved credit. Newton, who had developed his ideas
        first but published later, accused Leibniz of plagiarism. The Royal Society (led by Newton
        himself) ruled in Newton's favor. The controversy lasted decades and split European
        mathematics into two camps.

        Today, we recognize both as co-inventors. More importantly, we use **Leibniz's notation**
        because it's simply more intuitive and useful—proof that good notation matters.

        > 📚 **Further Reading**: [Newton's Principia Mathematica (1687)](https://archive.org/details/mathematicalprin00newtuoft)

        ### Making It Rigorous: The Limit

        Newton and Leibniz's methods worked, but they relied on vague notions of "infinitely small"
        quantities. It took another 150 years before mathematicians (particularly Cauchy and
        Weierstrass) made calculus rigorous using the concept of a **limit**.

        Instead of saying "$h$ is infinitely small," we say: "We can make the result as close as
        we want to the true answer by making $h$ sufficiently small." This avoids dividing by zero
        while capturing the same idea.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Part III: What is a Function?

        Before we can talk about derivatives, we need to understand what a **function** is.

        ### The Machine Metaphor

        A function is simply a rule that takes an input and produces exactly one output.
        Think of it as a machine: you put something in, something comes out.

        $$f: x \mapsto y$$

        **Key properties of functions:**
        1. **Every input gives exactly one output** — You can't have $f(2) = 4$ and $f(2) = 7$
        2. **The same input always gives the same output** — $f(2)$ is always the same value
        3. **Different inputs can give the same output** — $f(2) = f(-2) = 4$ for $f(x) = x^2$

        ### Common Function Families

        | Family | Example | Behavior |
        |--------|---------|----------|
        | **Polynomial** | $f(x) = x^2$, $g(x) = x^3 - 2x$ | Smooth curves, easy to compute |
        | **Trigonometric** | $\sin(x)$, $\cos(x)$ | Periodic (repeating) waves |
        | **Exponential** | $e^x$, $2^x$ | Rapid growth or decay |
        | **Logarithmic** | $\ln(x)$, $\log_{10}(x)$ | Slow growth, inverse of exponential |
        | **Rational** | $\frac{1}{x}$, $\frac{x^2+1}{x-1}$ | May have asymptotes and holes |

        Explore these functions below to build intuition for how they behave.
        """
    )
    return


@app.cell
def _(mo):
    function_dropdown = mo.ui.dropdown(
        options={
            "x²": "x**2",
            "x³": "x**3",
            "sin(x)": "sin(x)",
            "cos(x)": "cos(x)",
            "eˣ": "exp(x)",
            "ln(x)": "log(x)",
            "√x": "sqrt(x)",
            "1/x": "1/x",
            "x³ - 3x": "x**3 - 3*x",
        },
        value="x²",
        label="Choose a function:",
    )
    return function_dropdown,


@app.cell
def _(function_dropdown, mo):
    mo.hstack([
        mo.md("### Function Explorer"),
        function_dropdown,
    ])
    return


@app.cell
def _(function_dropdown, go, np, sp, Symbol):
    # Parse the selected function
    _x = Symbol('x')
    _expr = sp.sympify(function_dropdown.value)
    _f = sp.lambdify(_x, _expr, modules=['numpy'])

    # Generate plot data
    _x_vals = np.linspace(-4, 4, 500)
    with np.errstate(divide='ignore', invalid='ignore'):
        _y_vals = _f(_x_vals)
        _y_vals = np.where(np.abs(_y_vals) > 100, np.nan, _y_vals)

    # Create plot
    _fig = go.Figure()
    _fig.add_trace(go.Scatter(
        x=_x_vals, y=_y_vals,
        mode='lines',
        line={'color': '#00d4ff', 'width': 3},
        name=f'f(x) = {function_dropdown.value}',
    ))

    _fig.update_layout(
        paper_bgcolor='#16213e',
        plot_bgcolor='#1a1a2e',
        font={'color': '#eaeaea', 'family': 'JetBrains Mono, monospace'},
        title=f'Graph of f(x) = {function_dropdown.value}',
        xaxis={
            'gridcolor': '#2d3a4f', 'zerolinecolor': '#a0a0a0', 'zerolinewidth': 2,
            'title': 'x', 'range': [-4, 4]
        },
        yaxis={
            'gridcolor': '#2d3a4f', 'zerolinecolor': '#a0a0a0', 'zerolinewidth': 2,
            'title': 'f(x)', 'range': [-10, 10]
        },
        showlegend=True,
        legend={'bgcolor': 'rgba(22, 33, 62, 0.8)'},
    )
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        **Things to notice as you explore:**
        - **$x^2$** is symmetric about the y-axis (even function)
        - **$x^3$** is symmetric about the origin (odd function)
        - **$\sin(x)$** oscillates between -1 and 1 forever
        - **$e^x$** grows faster than any polynomial as $x \to \infty$
        - **$\ln(x)$** is only defined for positive $x$ (you can't take log of negative numbers)
        - **$1/x$** has a vertical asymptote at $x = 0$ (it "blows up" to infinity)
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Part IV: The Rate of Change

        ### Average vs. Instantaneous: The Central Question

        Imagine you're driving from New York to Boston, 215 miles apart. If the trip takes 4 hours,
        your **average speed** was:

        $$\text{Average speed} = \frac{\text{distance}}{\text{time}} = \frac{215 \text{ miles}}{4 \text{ hours}} = 53.75 \text{ mph}$$

        But this doesn't tell you how fast you were going at any particular moment. You probably
        went slower in city traffic and faster on the highway. At 2:37 PM, you might have been
        going 72 mph. At 3:15 PM, maybe you were stopped at a rest area (0 mph).

        **The central question of differential calculus**: How do we find the speed at a single instant?

        ### Why This Is Hard

        This seems almost paradoxical. Speed is "distance divided by time," but at a single instant:
        - No time passes → time interval = 0
        - No distance is covered → distance = 0
        - Speed = 0/0 → undefined!

        We seem to be stuck. We can't just plug in zero—that gives us nonsense.

        ### The Key Insight: Approach, Don't Arrive

        The genius of Newton and Leibniz was to realize: **don't actually let $h$ equal zero**.
        Instead, see what happens as $h$ gets closer and closer to zero.

        Think of it like this: if you want to know the speed at exactly 2:00 PM:
        - Measure your position at 2:00 PM and 2:01 PM → average speed over 1 minute
        - Measure at 2:00:00 and 2:00:01 → average speed over 1 second
        - Measure at 2:00:00.000 and 2:00:00.001 → average speed over 1 millisecond

        As the time interval shrinks, the average speed gets closer and closer to the
        **instantaneous speed**. The limit of this process is the derivative.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Secant Lines: The Geometric Picture

        Let's make this visual. Consider a car whose position at time $t$ is given by $s(t) = t^2$ meters.

        The average velocity between time $t$ and time $t + h$ is:

        $$v_{\text{avg}} = \frac{s(t+h) - s(t)}{h} = \frac{(t+h)^2 - t^2}{h}$$

        **Geometrically, this is the slope of the secant line** connecting two points on the curve:
        - Point 1: $(t, s(t))$
        - Point 2: $(t+h, s(t+h))$

        A **secant line** is simply a line that passes through two points on a curve.
        The slope of this line represents the average rate of change between those two points.

        As we make $h$ smaller and smaller:
        1. The two points get closer together
        2. The secant line rotates
        3. It approaches a line that touches the curve at just one point

        This limiting line is called the **tangent line**, and its slope is the **derivative**—
        the instantaneous rate of change.
        """
    )
    return


@app.cell
def _(go, np):
    def _create_secant_demo():
        """Create interactive secant-to-tangent visualization."""
        x = np.linspace(-1, 3, 300)
        y = x ** 2  # f(x) = x²

        x0 = 1.0  # Point of tangency
        y0 = x0 ** 2
        true_slope = 2 * x0  # Derivative of x² at x=1 is 2

        h_values = [2.0, 1.5, 1.0, 0.5, 0.25, 0.1, 0.05, 0.01]

        fig = go.Figure()

        # Function curve
        fig.add_trace(go.Scatter(
            x=x, y=y,
            mode='lines',
            line={'color': '#00d4ff', 'width': 3},
            name='f(x) = x²',
        ))

        # Tangent line (target)
        x_tan = np.array([-1, 3])
        y_tan = y0 + true_slope * (x_tan - x0)
        fig.add_trace(go.Scatter(
            x=x_tan, y=y_tan,
            mode='lines',
            line={'color': '#4ecdc4', 'width': 2, 'dash': 'dash'},
            name=f'Tangent (slope = {true_slope:.1f})',
        ))

        # Initial secant line
        h = h_values[0]
        x1 = x0 + h
        y1 = x1 ** 2
        slope = (y1 - y0) / h
        y_sec = y0 + slope * (x_tan - x0)

        fig.add_trace(go.Scatter(
            x=x_tan, y=y_sec,
            mode='lines',
            line={'color': '#ffe66d', 'width': 2},
            name=f'Secant (h = {h:.2f})',
        ))

        # Points
        fig.add_trace(go.Scatter(
            x=[x0], y=[y0],
            mode='markers',
            marker={'color': '#ff6b6b', 'size': 12},
            name='Fixed point (1, 1)',
        ))

        fig.add_trace(go.Scatter(
            x=[x1], y=[y1],
            mode='markers',
            marker={'color': '#ffe66d', 'size': 10},
            name='Moving point',
        ))

        # Create slider steps
        steps = []
        for h in h_values:
            x1 = x0 + h
            y1 = x1 ** 2
            slope = (y1 - y0) / h
            y_sec = y0 + slope * (x_tan - x0)

            step = {
                "method": "update",
                "args": [
                    {"x": [x, x_tan, x_tan, [x0], [x1]], "y": [y, y_tan, y_sec, [y0], [y1]]},
                    {"title": f"h = {h:.2f} | Secant slope = {slope:.4f} | Tangent slope = {true_slope:.1f}"}
                ],
                "label": f"{h:.2f}",
            }
            steps.append(step)

        fig.update_layout(
            paper_bgcolor='#16213e',
            plot_bgcolor='#1a1a2e',
            font={'color': '#eaeaea', 'family': 'JetBrains Mono, monospace'},
            title=f"h = {h_values[0]:.2f} | Secant slope = {((x0+h_values[0])**2 - y0)/h_values[0]:.4f} | Tangent slope = {true_slope:.1f}",
            xaxis={'gridcolor': '#2d3a4f', 'zerolinecolor': '#a0a0a0', 'title': 'x'},
            yaxis={'gridcolor': '#2d3a4f', 'zerolinecolor': '#a0a0a0', 'title': 'y', 'range': [-1, 10]},
            sliders=[{
                "active": 0,
                "currentvalue": {"prefix": "h = ", "visible": True},
                "pad": {"b": 10, "t": 50},
                "steps": steps,
                "bgcolor": "#16213e",
                "font": {"color": "#eaeaea"},
            }],
        )

        return fig

    _create_secant_demo()
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        **Try it!** Use the slider above to decrease $h$. Watch as:
        1. The **moving point** (yellow) approaches the **fixed point** (red)
        2. The **secant line** (yellow) rotates toward the **tangent line** (teal)
        3. The **secant slope** approaches the **tangent slope** (2.0)

        This is the essence of the derivative: **the limit of the secant slope as $h$ approaches zero**.

        Notice that we never actually set $h = 0$. We just get arbitrarily close. This is what
        mathematicians mean by a "limit"—the value we approach, not the value we reach.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Part V: The Limit Process

        ### The Formal Definition of the Derivative

        We've seen intuitively that the secant slope approaches the tangent slope.
        Now let's make this precise with mathematical notation.

        The **derivative** of $f(x)$ at point $x$ is defined as:

        $$\boxed{f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}}$$

        Let's break down this notation:
        - **$f'(x)$** — This is the derivative, read as "f prime of x"
        - **$\lim_{h \to 0}$** — "The limit as h approaches zero"
        - **$\frac{f(x+h) - f(x)}{h}$** — This is called the **difference quotient**

        The difference quotient $\frac{f(x+h) - f(x)}{h}$ measures:
        - **Numerator**: How much $f$ changes when we move from $x$ to $x+h$
        - **Denominator**: How far we moved (which is $h$)
        - **Ratio**: The average rate of change over the interval $[x, x+h]$

        ### Working Through an Example

        Let's compute the derivative of $f(x) = x^2$ at $x = 1$ step by step:

        $$f'(1) = \lim_{h \to 0} \frac{f(1+h) - f(1)}{h}$$

        **Step 1**: Substitute $f(x) = x^2$
        $$= \lim_{h \to 0} \frac{(1+h)^2 - 1^2}{h}$$

        **Step 2**: Expand $(1+h)^2 = 1 + 2h + h^2$
        $$= \lim_{h \to 0} \frac{1 + 2h + h^2 - 1}{h}$$

        **Step 3**: Simplify the numerator
        $$= \lim_{h \to 0} \frac{2h + h^2}{h}$$

        **Step 4**: Factor out $h$ from the numerator
        $$= \lim_{h \to 0} \frac{h(2 + h)}{h}$$

        **Step 5**: Cancel the $h$ terms (valid since $h \neq 0$ in the limit)
        $$= \lim_{h \to 0} (2 + h)$$

        **Step 6**: Now we can safely let $h \to 0$
        $$= 2$$

        **The derivative of $x^2$ at $x = 1$ is 2.** This means the slope of the tangent line
        at the point $(1, 1)$ is 2, and the function is increasing at a rate of 2 units of $y$
        per unit of $x$ at that instant.
        """
    )
    return


@app.cell
def _(mo, pl):
    # Table showing h approaching 0
    _h_values = [1.0, 0.5, 0.1, 0.05, 0.01, 0.001, 0.0001]
    _slopes = [(((1 + h) ** 2 - 1) / h) for h in _h_values]

    _df = pl.DataFrame({
        "h": _h_values,
        "f(1+h) = (1+h)²": [(1 + h) ** 2 for h in _h_values],
        "f(1) = 1": [1.0] * len(_h_values),
        "Slope = [f(1+h) - f(1)] / h": [round(s, 6) for s in _slopes],
    })

    mo.vstack([
        mo.md(r"""
### Numerical Evidence: Slopes Approaching 2

The table below shows what happens as $h$ gets smaller. Notice how the slope gets
closer and closer to exactly 2, confirming our algebraic calculation.
        """),
        mo.ui.table(_df),
    ])
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Why Does the Cancellation Work?

        You might wonder: "We cancelled $h$ from numerator and denominator, but isn't $h$ approaching
        zero? Isn't that like dividing by zero?"

        The key insight is that **we're taking a limit, not evaluating at $h = 0$**.

        When we write $\lim_{h \to 0}$, we're asking: "What value does this expression approach
        as $h$ gets arbitrarily close to (but never equal to) zero?"

        For any $h \neq 0$, the cancellation $\frac{h(2+h)}{h} = 2 + h$ is perfectly valid.
        And since $2 + h$ approaches 2 as $h$ approaches 0, the limit is 2.

        This is why limits are so powerful: they let us reason about what happens "infinitely
        close to" a point without ever having to evaluate exactly at that point.
        """
    )
    return


@app.cell
def _(go, np):
    def _animate_limit():
        """Animate h approaching 0."""
        x = np.linspace(-0.5, 2.5, 300)
        y = x ** 2

        x0 = 1.0
        y0 = 1.0
        true_slope = 2.0

        num_frames = 60
        h_values = np.exp(np.linspace(np.log(1.5), np.log(0.01), num_frames))

        fig = go.Figure()

        # Function
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', line={'color': '#00d4ff', 'width': 3}, name='f(x) = x²'))

        # Tangent
        x_line = np.array([-0.5, 2.5])
        y_tan = y0 + true_slope * (x_line - x0)
        fig.add_trace(go.Scatter(x=x_line, y=y_tan, mode='lines',
                                  line={'color': '#4ecdc4', 'width': 2, 'dash': 'dash'}, name='Tangent'))

        # Secant
        h = h_values[0]
        slope = (((x0 + h) ** 2 - y0) / h)
        y_sec = y0 + slope * (x_line - x0)
        fig.add_trace(go.Scatter(x=x_line, y=y_sec, mode='lines',
                                  line={'color': '#ffe66d', 'width': 3}, name='Secant'))

        # Points
        fig.add_trace(go.Scatter(x=[x0], y=[y0], mode='markers',
                                  marker={'color': '#ff6b6b', 'size': 14}, name='(1, 1)'))
        fig.add_trace(go.Scatter(x=[x0 + h], y=[(x0 + h) ** 2], mode='markers',
                                  marker={'color': '#ffe66d', 'size': 10}, name='Moving'))

        frames = []
        for i, h in enumerate(h_values):
            x1 = x0 + h
            y1 = x1 ** 2
            slope = (y1 - y0) / h
            y_sec = y0 + slope * (x_line - x0)

            frame = go.Frame(
                data=[
                    go.Scatter(x=x, y=y),
                    go.Scatter(x=x_line, y=y_tan),
                    go.Scatter(x=x_line, y=y_sec),
                    go.Scatter(x=[x0], y=[y0]),
                    go.Scatter(x=[x1], y=[y1]),
                ],
                name=str(i),
                layout={"title": f"h = {h:.4f} | Slope = {slope:.4f} → 2.0000"}
            )
            frames.append(frame)

        fig.frames = frames

        fig.update_layout(
            paper_bgcolor='#16213e',
            plot_bgcolor='#1a1a2e',
            font={'color': '#eaeaea', 'family': 'JetBrains Mono, monospace'},
            title=f"The Limit: h → 0",
            xaxis={'gridcolor': '#2d3a4f', 'zerolinecolor': '#a0a0a0', 'title': 'x', 'range': [-0.5, 2.5]},
            yaxis={'gridcolor': '#2d3a4f', 'zerolinecolor': '#a0a0a0', 'title': 'y', 'range': [-0.5, 5]},
            updatemenus=[{
                "type": "buttons",
                "showactive": False,
                "y": 1.15,
                "x": 0.5,
                "xanchor": "center",
                "buttons": [
                    {"label": "▶ Play", "method": "animate",
                     "args": [None, {"frame": {"duration": 50}, "transition": {"duration": 30}}]},
                    {"label": "⏸ Pause", "method": "animate",
                     "args": [[None], {"frame": {"duration": 0}, "mode": "immediate"}]},
                ],
                "font": {"color": "#eaeaea"},
                "bgcolor": "#16213e",
            }],
        )

        return fig

    _animate_limit()
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        **What the animation shows:**

        Press **Play** to watch the limit process in action. As $h$ shrinks from 1.5 down to 0.01:

        1. The **yellow secant line** rotates, approaching the **teal tangent line**
        2. The **slope value** in the title converges toward exactly 2
        3. The **moving point** slides along the parabola toward the fixed point

        This visual demonstrates the core idea: we never reach $h = 0$, but we can get
        arbitrarily close. The slope approaches 2 as a **limit**, not as a final value.

        **Key insight**: The limit exists because the secant slopes form a convergent sequence.
        No matter how small we make $h$, the pattern continues—the slopes keep getting closer to 2.
        This consistency is what allows us to define the derivative.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Part VI: The Power Rule

        ### Computing Derivatives Efficiently

        Using the limit definition every time would be tedious. Fortunately, mathematicians have
        discovered patterns that let us compute derivatives quickly.

        **The Power Rule** is the most fundamental:

        $$\boxed{\text{If } f(x) = x^n, \text{ then } f'(x) = nx^{n-1}}$$

        In words: "Bring down the exponent as a coefficient, then reduce the exponent by 1."

        **Examples:**
        - $f(x) = x^2 \Rightarrow f'(x) = 2x^1 = 2x$
        - $f(x) = x^3 \Rightarrow f'(x) = 3x^2$
        - $f(x) = x^5 \Rightarrow f'(x) = 5x^4$
        - $f(x) = x^{100} \Rightarrow f'(x) = 100x^{99}$

        ### Proof of the Power Rule

        Let's prove this for any positive integer $n$. We'll use the limit definition:

        $$f'(x) = \lim_{h \to 0} \frac{(x+h)^n - x^n}{h}$$

        The binomial theorem tells us:
        $$(x+h)^n = x^n + nx^{n-1}h + \frac{n(n-1)}{2}x^{n-2}h^2 + \cdots + h^n$$

        All terms after the first two contain $h^2$ or higher powers of $h$. Substituting:

        $$f'(x) = \lim_{h \to 0} \frac{x^n + nx^{n-1}h + (\text{terms with } h^2, h^3, \ldots) - x^n}{h}$$

        The $x^n$ terms cancel:

        $$= \lim_{h \to 0} \frac{nx^{n-1}h + (\text{terms with } h^2, h^3, \ldots)}{h}$$

        Factor out $h$:

        $$= \lim_{h \to 0} \left[ nx^{n-1} + (\text{terms with } h, h^2, \ldots) \right]$$

        As $h \to 0$, all terms containing $h$ vanish, leaving:

        $$f'(x) = nx^{n-1} \quad \square$$
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Interactive Exploration: The Power Rule

        The visualization below shows both a function $f(x) = x^n$ (in blue) and its derivative
        $f'(x) = nx^{n-1}$ (in red) on the same axes.

        Use the slider to change the power $n$ and observe:
        - How the shape of the function changes with different powers
        - The relationship between where $f(x)$ is increasing/decreasing and where $f'(x)$ is positive/negative
        - How the derivative is always one degree lower than the original function
        """
    )
    return


@app.cell
def _(mo):
    power_slider = mo.ui.slider(
        start=1, stop=6, step=1, value=2,
        label="Power n:",
        show_value=True,
    )
    return power_slider,


@app.cell
def _(mo, power_slider):
    mo.hstack([
        mo.md("**Choose a power:**"),
        power_slider,
    ])
    return


@app.cell
def _(go, np, power_slider):
    _n = power_slider.value
    _x = np.linspace(-2, 2, 300)

    _y_f = _x ** _n
    _y_fp = _n * _x ** (_n - 1) if _n > 0 else np.zeros_like(_x)

    # Clip for display
    _y_f = np.clip(_y_f, -15, 15)
    _y_fp = np.clip(_y_fp, -15, 15)

    _fig = go.Figure()

    _fig.add_trace(go.Scatter(
        x=_x, y=_y_f,
        mode='lines',
        line={'color': '#00d4ff', 'width': 3},
        name=f'f(x) = x^{_n}',
    ))

    _fig.add_trace(go.Scatter(
        x=_x, y=_y_fp,
        mode='lines',
        line={'color': '#ff6b6b', 'width': 3},
        name=f"f'(x) = {_n}x^{_n-1}",
    ))

    _fig.update_layout(
        paper_bgcolor='#16213e',
        plot_bgcolor='#1a1a2e',
        font={'color': '#eaeaea', 'family': 'JetBrains Mono, monospace'},
        title=f"Power Rule: f(x) = x^{_n}, f'(x) = {_n}x^{_n-1}",
        xaxis={'gridcolor': '#2d3a4f', 'zerolinecolor': '#a0a0a0', 'title': 'x'},
        yaxis={'gridcolor': '#2d3a4f', 'zerolinecolor': '#a0a0a0', 'title': 'y', 'range': [-10, 10]},
        showlegend=True,
        legend={'bgcolor': 'rgba(22, 33, 62, 0.8)'},
    )
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        **Observations** (try different values of n):

        - **$n = 1$**: $f(x) = x$, $f'(x) = 1$. A straight line has constant slope.

        - **$n = 2$**: $f(x) = x^2$, $f'(x) = 2x$. The derivative is a line through the origin.
          Where $f'(x) > 0$ (right side), the parabola is increasing. Where $f'(x) < 0$ (left side),
          it's decreasing. At $x = 0$, the derivative is zero—this is the minimum.

        - **$n = 3$**: $f(x) = x^3$, $f'(x) = 3x^2$. The derivative is always non-negative
          (a parabola opening upward), so $x^3$ never decreases—except at $x = 0$ where it
          momentarily "pauses" (derivative = 0).

        - **Higher powers**: The derivative is always one degree lower than the original function.
          A polynomial of degree $n$ has a derivative of degree $n-1$.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### The Complete Toolkit: Derivative Rules

        The power rule is just one of many rules. Here's the complete toolkit for computing derivatives:

        | Rule | Function | Derivative | Example |
        |------|----------|------------|---------|
        | **Constant** | $c$ | $0$ | $(5)' = 0$ |
        | **Power** | $x^n$ | $nx^{n-1}$ | $(x^3)' = 3x^2$ |
        | **Constant Multiple** | $cf(x)$ | $cf'(x)$ | $(3x^2)' = 3 \cdot 2x = 6x$ |
        | **Sum** | $f(x) + g(x)$ | $f'(x) + g'(x)$ | $(x^2 + x)' = 2x + 1$ |
        | **Difference** | $f(x) - g(x)$ | $f'(x) - g'(x)$ | $(x^2 - x)' = 2x - 1$ |
        | **Product** | $f(x)g(x)$ | $f'(x)g(x) + f(x)g'(x)$ | See below |
        | **Quotient** | $\frac{f(x)}{g(x)}$ | $\frac{f'(x)g(x) - f(x)g'(x)}{[g(x)]^2}$ | See below |
        | **Exponential** | $e^x$ | $e^x$ | $(e^x)' = e^x$ |
        | **Natural Log** | $\ln(x)$ | $\frac{1}{x}$ | $(\ln x)' = \frac{1}{x}$ |
        | **Sine** | $\sin(x)$ | $\cos(x)$ | $(\sin x)' = \cos x$ |
        | **Cosine** | $\cos(x)$ | $-\sin(x)$ | $(\cos x)' = -\sin x$ |

        **Note on $e^x$**: The exponential function $e^x$ is special—it's the only function that equals
        its own derivative! This is why $e$ (approximately 2.71828) appears throughout mathematics.

        ### Product Rule Example

        Find the derivative of $f(x) = x^2 \sin(x)$:

        Using the product rule with $u = x^2$ and $v = \sin(x)$:
        $$f'(x) = u'v + uv' = (2x)(\sin x) + (x^2)(\cos x) = 2x\sin(x) + x^2\cos(x)$$

        ### Quotient Rule Example

        Find the derivative of $f(x) = \frac{x^2}{x + 1}$:

        Using the quotient rule with $u = x^2$ and $v = x + 1$:
        $$\begin{aligned}
        f'(x) &= \frac{u'v - uv'}{v^2} \\
        &= \frac{(2x)(x+1) - (x^2)(1)}{(x+1)^2} \\
        &= \frac{2x^2 + 2x - x^2}{(x+1)^2} \\
        &= \frac{x^2 + 2x}{(x+1)^2}
        \end{aligned}$$

        ### When to Use Which Rule

        - **Sum/Difference**: When functions are added or subtracted
        - **Product**: When functions are multiplied (like $x^2 \sin(x)$)
        - **Quotient**: When one function divides another (like $\frac{x^2}{x+1}$)
        - **Chain**: When functions are nested (like $\sin(x^2)$) — covered next!
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Part VII: The Chain Rule

        ### When Functions Are Nested Inside Each Other

        What if we have a function inside another function, like $f(x) = \sin(x^2)$?

        Here, we first compute $x^2$, then take the sine of the result. This is called a
        **composite function**, written as $(f \circ g)(x) = f(g(x))$.

        For $\sin(x^2)$:
        - **Inner function** (computed first): $g(x) = x^2$
        - **Outer function** (computed second): $f(u) = \sin(u)$
        - **Composition**: $f(g(x)) = \sin(x^2)$

        ### The Chain Rule

        The **Chain Rule** tells us how to differentiate composite functions:

        $$\boxed{\frac{d}{dx}[f(g(x))] = f'(g(x)) \cdot g'(x)}$$

        In words: "Derivative of the outer (evaluated at the inner) times derivative of the inner."

        Using Leibniz notation makes this even clearer. If $y = f(u)$ and $u = g(x)$:

        $$\frac{dy}{dx} = \frac{dy}{du} \cdot \frac{du}{dx}$$

        This looks like the $du$'s "cancel"—and while that's not quite rigorous, it's a useful mnemonic.

        ### Worked Example: $y = \sin(x^2)$

        **Step 1**: Identify the parts
        - Inner function: $u = g(x) = x^2$
        - Outer function: $y = f(u) = \sin(u)$

        **Step 2**: Find each derivative
        - $\frac{dy}{du} = \cos(u) = \cos(x^2)$ (derivative of sine is cosine)
        - $\frac{du}{dx} = 2x$ (power rule)

        **Step 3**: Multiply them together
        $$\begin{aligned}
        \frac{dy}{dx} &= \frac{dy}{du} \cdot \frac{du}{dx} \\
        &= \cos(x^2) \cdot 2x \\
        &= 2x\cos(x^2)
        \end{aligned}$$

        ### Why the Chain Rule Works (Intuition)

        Think about rates of change:
        - If $u$ changes at rate $\frac{du}{dx}$ with respect to $x$
        - And $y$ changes at rate $\frac{dy}{du}$ with respect to $u$
        - Then $y$ changes at rate $\frac{dy}{du} \cdot \frac{du}{dx}$ with respect to $x$

        It's like unit conversion: if a car goes 60 miles per hour and there are 1.6 km per mile,
        it goes $60 \times 1.6 = 96$ km per hour.
        """
    )
    return


@app.cell
def _(go, np):
    # Chain rule visualization: sin(x²)
    _x = np.linspace(-2.5, 2.5, 400)

    _inner = _x ** 2  # g(x) = x²
    _composite = np.sin(_x ** 2)  # f(g(x)) = sin(x²)
    _derivative = 2 * _x * np.cos(_x ** 2)  # f'(g(x)) * g'(x)

    _fig = go.Figure()

    _fig.add_trace(go.Scatter(
        x=_x, y=np.clip(_inner, -5, 5),
        mode='lines',
        line={'color': '#95e1d3', 'width': 2},
        name='g(x) = x² (inner)',
    ))

    _fig.add_trace(go.Scatter(
        x=_x, y=_composite,
        mode='lines',
        line={'color': '#00d4ff', 'width': 3},
        name='f(g(x)) = sin(x²)',
    ))

    _fig.add_trace(go.Scatter(
        x=_x, y=_derivative,
        mode='lines',
        line={'color': '#ff6b6b', 'width': 3},
        name="(f∘g)'(x) = 2x·cos(x²)",
    ))

    _fig.update_layout(
        paper_bgcolor='#16213e',
        plot_bgcolor='#1a1a2e',
        font={'color': '#eaeaea', 'family': 'JetBrains Mono, monospace'},
        title="Chain Rule: (f∘g)'(x) = f'(g(x)) · g'(x)",
        xaxis={'gridcolor': '#2d3a4f', 'zerolinecolor': '#a0a0a0', 'title': 'x'},
        yaxis={'gridcolor': '#2d3a4f', 'zerolinecolor': '#a0a0a0', 'title': 'y', 'range': [-5, 5]},
        showlegend=True,
        legend={'bgcolor': 'rgba(22, 33, 62, 0.8)'},
    )
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        **Observations from the graph:**

        - The composite function $\sin(x^2)$ oscillates faster as $|x|$ increases (because $x^2$
          grows, making the sine cycle through more periods)

        - The derivative $2x\cos(x^2)$ oscillates too, but it also grows in magnitude away from
          the origin (because of the $2x$ factor)

        - Where the composite function has a horizontal tangent (peaks and troughs), the
          derivative crosses zero
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Part VIII: Geometric Interpretation

        ### The Tangent Line as Best Linear Approximation

        The derivative has a beautiful geometric meaning: **the tangent line is the best linear
        approximation to a function at a point**.

        Imagine zooming in on a smooth curve at a point. As you zoom in more and more, the curve
        looks increasingly like a straight line. That line is the tangent line, and its slope
        is the derivative.

        ### The Linear Approximation Formula

        If we know $f(a)$ and $f'(a)$, we can approximate $f(x)$ for $x$ near $a$:

        $$\boxed{f(x) \approx f(a) + f'(a)(x - a)}$$

        This is called the **linear approximation** or **tangent line approximation**.

        **Why does this work?**
        - $f(a)$ gives us the correct value at $x = a$
        - $f'(a)$ gives us the correct slope at $x = a$
        - The formula describes a line through $(a, f(a))$ with slope $f'(a)$

        For $x$ close to $a$, this line stays close to the actual function. The approximation
        gets worse as $x$ moves farther from $a$.

        ### Practical Uses

        Linear approximation is used constantly in science and engineering:
        - Physicists simplify equations by approximating $\sin(\theta) \approx \theta$ for small angles
        - Engineers linearize nonlinear systems to make them easier to analyze
        - Numerical methods use tangent lines to find roots (Newton's method)

        ### Interactive Exploration: Moving the Tangent Point

        The visualization below shows $f(x) = x^3 - x$ with a tangent line that you can move
        along the curve. The stars mark the **critical points** where $f'(x) = 0$.

        As you move the slider, notice:
        - The slope changes sign as you cross the critical points
        - The tangent is horizontal (slope = 0) exactly at the stars
        - The function is increasing where the slope is positive, decreasing where it's negative
        """
    )
    return


@app.cell
def _(mo):
    tangent_point = mo.ui.slider(
        start=-2.0, stop=2.0, step=0.1, value=1.0,
        label="Touch point x₀:",
        show_value=True,
    )
    return tangent_point,


@app.cell
def _(mo, tangent_point):
    mo.hstack([
        mo.md("### Interactive Tangent Line"),
        tangent_point,
    ])
    return


@app.cell
def _(go, np, tangent_point):
    _x0 = tangent_point.value
    _x = np.linspace(-3, 3, 300)
    _y = _x ** 3 - _x  # f(x) = x³ - x

    _y0 = _x0 ** 3 - _x0
    _slope = 3 * _x0 ** 2 - 1  # f'(x) = 3x² - 1

    # Tangent line
    _x_tan = np.array([-3, 3])
    _y_tan = _y0 + _slope * (_x_tan - _x0)

    _fig = go.Figure()

    _fig.add_trace(go.Scatter(
        x=_x, y=_y,
        mode='lines',
        line={'color': '#00d4ff', 'width': 3},
        name='f(x) = x³ - x',
    ))

    _fig.add_trace(go.Scatter(
        x=_x_tan, y=_y_tan,
        mode='lines',
        line={'color': '#4ecdc4', 'width': 2, 'dash': 'dash'},
        name=f'Tangent (slope = {_slope:.2f})',
    ))

    _fig.add_trace(go.Scatter(
        x=[_x0], y=[_y0],
        mode='markers',
        marker={'color': '#ffe66d', 'size': 14},
        name=f'({_x0:.1f}, {_y0:.2f})',
    ))

    # Mark critical points where f'(x) = 0
    _crit_x = np.array([-1/np.sqrt(3), 1/np.sqrt(3)])
    _crit_y = _crit_x ** 3 - _crit_x

    _fig.add_trace(go.Scatter(
        x=_crit_x, y=_crit_y,
        mode='markers',
        marker={'color': '#f38181', 'size': 10, 'symbol': 'star'},
        name="Critical points (f'=0)",
    ))

    _fig.update_layout(
        paper_bgcolor='#16213e',
        plot_bgcolor='#1a1a2e',
        font={'color': '#eaeaea', 'family': 'JetBrains Mono, monospace'},
        title=f"Tangent at x = {_x0:.1f} | Slope = {_slope:.2f}",
        xaxis={'gridcolor': '#2d3a4f', 'zerolinecolor': '#a0a0a0', 'title': 'x', 'range': [-3, 3]},
        yaxis={'gridcolor': '#2d3a4f', 'zerolinecolor': '#a0a0a0', 'title': 'y', 'range': [-4, 4]},
        showlegend=True,
        legend={'bgcolor': 'rgba(22, 33, 62, 0.8)'},
    )
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        **Key observations:**

        - **Horizontal tangents** occur where the slope is zero. For $f(x) = x^3 - x$, we have
          $f'(x) = 3x^2 - 1 = 0$ when $x = \pm\frac{1}{\sqrt{3}} \approx \pm 0.577$.
          These points are marked with stars.

        - At the **left critical point** ($x \approx -0.577$), the function reaches a **local maximum**
          — it's higher than nearby points.

        - At the **right critical point** ($x \approx 0.577$), the function reaches a **local minimum**
          — it's lower than nearby points.

        - When the slope is **positive**, the function is **increasing** (going uphill left to right).

        - When the slope is **negative**, the function is **decreasing** (going downhill left to right).

        This connection between the sign of the derivative and the behavior of the function is
        fundamental to understanding and optimizing functions.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Part IX: Applications — Projectile Motion

        ### Physics: Where Calculus Was Born

        Newton invented calculus specifically to solve physics problems—particularly to understand
        motion and gravity. Let's see how calculus describes the motion of a thrown ball.

        ### The Setup

        When you throw a ball straight up with initial velocity $v_0$:

        **Position** (where is the ball?):
        $$y(t) = v_0 t - \frac{1}{2}gt^2$$

        where $g \approx 9.8$ m/s² is the acceleration due to gravity.

        This formula comes from physics, but let's see what calculus tells us about it.

        ### Finding Velocity: The First Derivative

        **Velocity** is the rate of change of position—how fast the position is changing:

        $$v(t) = y'(t) = \frac{d}{dt}\left[v_0 t - \frac{1}{2}gt^2\right]$$

        Using the power rule:
        $$v(t) = v_0 - gt$$

        This tells us:
        - At $t = 0$, velocity is $v_0$ (initial velocity) — the ball starts moving upward
        - Velocity decreases by $g$ each second (gravity slows it down)
        - When $v(t) = 0$, the ball momentarily stops at its peak
        - After that, velocity becomes negative (ball falls down)

        ### Finding Acceleration: The Second Derivative

        **Acceleration** is the rate of change of velocity:

        $$a(t) = v'(t) = y''(t) = \frac{d}{dt}[v_0 - gt] = -g$$

        The acceleration is constant! It's just gravity, pulling down at $g$ m/s² the whole time.
        This is Newton's insight: gravity provides a constant downward acceleration.

        ### The Peak: When Does the Ball Stop Rising?

        The ball reaches its maximum height when $v(t) = 0$:
        $$v_0 - gt = 0 \implies t = \frac{v_0}{g}$$

        This is a general principle: **maxima and minima occur where the derivative is zero**.
        """
    )
    return


@app.cell
def _(go, np):
    # Projectile motion animation
    _v0 = 20  # m/s
    _g = 9.8  # m/s²
    _t_flight = 2 * _v0 / _g
    _t = np.linspace(0, _t_flight, 50)

    _y = _v0 * _t - 0.5 * _g * _t ** 2  # Position
    _v = _v0 - _g * _t  # Velocity

    _fig = go.Figure()

    # Position vs time
    _fig.add_trace(go.Scatter(
        x=_t, y=_y,
        mode='lines',
        line={'color': '#00d4ff', 'width': 3},
        name='Position y(t)',
    ))

    # Velocity vs time
    _fig.add_trace(go.Scatter(
        x=_t, y=_v,
        mode='lines',
        line={'color': '#ff6b6b', 'width': 3},
        name='Velocity v(t) = y\'(t)',
    ))

    # Acceleration (constant)
    _fig.add_trace(go.Scatter(
        x=_t, y=np.full_like(_t, -_g),
        mode='lines',
        line={'color': '#4ecdc4', 'width': 2, 'dash': 'dash'},
        name='Acceleration a(t) = y\'\'(t)',
    ))

    # Peak point
    _t_peak = _v0 / _g
    _y_peak = _v0 * _t_peak - 0.5 * _g * _t_peak ** 2
    _fig.add_trace(go.Scatter(
        x=[_t_peak], y=[_y_peak],
        mode='markers+text',
        marker={'color': '#ffe66d', 'size': 12},
        text=['Max height (v=0)'],
        textposition='top center',
        textfont={'color': '#ffe66d'},
        name='Peak',
    ))

    _fig.add_hline(y=0, line_dash="dot", line_color="#a0a0a0", opacity=0.5)

    _fig.update_layout(
        paper_bgcolor='#16213e',
        plot_bgcolor='#1a1a2e',
        font={'color': '#eaeaea', 'family': 'JetBrains Mono, monospace'},
        title=f"Projectile Motion: v₀ = {_v0} m/s",
        xaxis={'gridcolor': '#2d3a4f', 'zerolinecolor': '#a0a0a0', 'title': 'Time (s)'},
        yaxis={'gridcolor': '#2d3a4f', 'zerolinecolor': '#a0a0a0', 'title': 'y (m) or v (m/s)'},
        showlegend=True,
        legend={'bgcolor': 'rgba(22, 33, 62, 0.8)'},
    )
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        **Reading the graph:**

        - **Blue curve (position)**: Parabola showing height over time. Maximum at the peak.

        - **Red curve (velocity)**: Straight line decreasing from +20 to -20 m/s.
          Crosses zero exactly at the peak—this is where the derivative of position is zero,
          so position has a maximum.

        - **Teal line (acceleration)**: Constant at -9.8 m/s². Gravity never changes.

        **Physical insights from calculus:**

        1. The ball spends equal time going up and coming down (symmetry of the parabola)

        2. The ball has the same speed at any height going up as coming down (conservation of energy)

        3. At the peak, velocity is zero but acceleration isn't—the ball is still being pulled down,
           it just hasn't started moving down yet

        This is the power of calculus: from a position formula, we can derive velocity and
        acceleration, understanding the complete motion.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Part X: Optimization

        ### Finding Maxima and Minima

        One of the most powerful applications of derivatives is **optimization**—finding where
        functions reach their maximum or minimum values.

        Real-world optimization problems include:
        - Maximizing profit or efficiency
        - Minimizing cost or waste
        - Finding the best dimensions for a container
        - Optimizing routes or schedules

        ### The Critical Point Method

        From our exploration of tangent lines, we know that horizontal tangent lines (slope = 0)
        occur at peaks and valleys. This gives us a method:

        **Step 1**: Find **critical points** where $f'(x) = 0$

        **Step 2**: Determine whether each critical point is a maximum, minimum, or neither

        ### The Second Derivative Test

        The **second derivative** $f''(x)$ tells us about **concavity**—whether the function
        curves upward or downward:

        - $f''(x) > 0$: Function is **concave up** (curves upward like $\cup$)
        - $f''(x) < 0$: Function is **concave down** (curves downward like $\cap$)

        At a critical point where $f'(c) = 0$:

        | Second Derivative | Concavity | Type of Critical Point |
        |-------------------|-----------|------------------------|
        | $f''(c) > 0$ | Concave up | **Local minimum** (valley) |
        | $f''(c) < 0$ | Concave down | **Local maximum** (peak) |
        | $f''(c) = 0$ | Inconclusive | Need further analysis |

        **Intuition**: If you're at a point where the slope is zero and the function is curving
        upward, you must be at the bottom of a valley. If it's curving downward, you're at the
        top of a hill.

        ### Worked Example: $f(x) = x^3 - 3x$

        **Step 1**: Find $f'(x)$
        $$f'(x) = 3x^2 - 3 = 3(x^2 - 1) = 3(x-1)(x+1)$$

        **Step 2**: Find critical points (where $f'(x) = 0$)
        $$3(x-1)(x+1) = 0 \implies x = 1 \text{ or } x = -1$$

        **Step 3**: Find $f''(x)$
        $$f''(x) = 6x$$

        **Step 4**: Apply the second derivative test
        - At $x = -1$: $f''(-1) = -6 < 0$ → **local maximum**
        - At $x = 1$: $f''(1) = 6 > 0$ → **local minimum**

        **Step 5**: Find the actual values
        - Maximum: $f(-1) = (-1)^3 - 3(-1) = -1 + 3 = 2$
        - Minimum: $f(1) = (1)^3 - 3(1) = 1 - 3 = -2$
        """
    )
    return


@app.cell
def _(go, np):
    # Optimization example: f(x) = x³ - 3x
    _x = np.linspace(-2.5, 2.5, 300)
    _y = _x ** 3 - 3 * _x  # f(x)
    _y_prime = 3 * _x ** 2 - 3  # f'(x)
    _y_double_prime = 6 * _x  # f''(x)

    _fig = go.Figure()

    # Function
    _fig.add_trace(go.Scatter(
        x=_x, y=_y,
        mode='lines',
        line={'color': '#00d4ff', 'width': 3},
        name='f(x) = x³ - 3x',
    ))

    # First derivative
    _fig.add_trace(go.Scatter(
        x=_x, y=_y_prime,
        mode='lines',
        line={'color': '#ff6b6b', 'width': 2},
        name="f'(x) = 3x² - 3",
    ))

    # Second derivative
    _fig.add_trace(go.Scatter(
        x=_x, y=_y_double_prime,
        mode='lines',
        line={'color': '#4ecdc4', 'width': 2, 'dash': 'dash'},
        name="f''(x) = 6x",
    ))

    # Critical points
    # f'(x) = 0 when x = ±1
    _crit_points = [
        (-1, 2, "Maximum\nf''(-1) = -6 < 0"),
        (1, -2, "Minimum\nf''(1) = 6 > 0"),
    ]

    for _xc, _yc, _label in _crit_points:
        _color = '#f38181' if 'Max' in _label else '#95e1d3'
        _fig.add_trace(go.Scatter(
            x=[_xc], y=[_yc],
            mode='markers+text',
            marker={'color': _color, 'size': 14, 'symbol': 'star'},
            text=[_label],
            textposition='top center' if 'Max' in _label else 'bottom center',
            textfont={'color': _color, 'size': 11},
            showlegend=False,
        ))

    _fig.add_hline(y=0, line_dash="dot", line_color="#a0a0a0", opacity=0.5)

    _fig.update_layout(
        paper_bgcolor='#16213e',
        plot_bgcolor='#1a1a2e',
        font={'color': '#eaeaea', 'family': 'JetBrains Mono, monospace'},
        title="Optimization: Finding Extrema with the Second Derivative Test",
        xaxis={'gridcolor': '#2d3a4f', 'zerolinecolor': '#a0a0a0', 'title': 'x'},
        yaxis={'gridcolor': '#2d3a4f', 'zerolinecolor': '#a0a0a0', 'title': 'y', 'range': [-5, 5]},
        showlegend=True,
        legend={'bgcolor': 'rgba(22, 33, 62, 0.8)', 'x': 1.02},
    )
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        **Reading the optimization graph:**

        1. **Blue curve** ($f(x)$): The original function, with a peak at $x=-1$ and a valley at $x=1$

        2. **Red curve** ($f'(x)$): Crosses zero exactly at the critical points $x = \pm 1$.
           Notice that $f'$ is positive when $f$ is increasing, and negative when $f$ is decreasing.

        3. **Teal line** ($f''(x) = 6x$): Tells us the concavity.
           - Negative for $x < 0$ → $f$ curves downward there
           - Positive for $x > 0$ → $f$ curves upward there
           - At $x = -1$, $f'' = -6 < 0$, confirming it's a maximum
           - At $x = 1$, $f'' = 6 > 0$, confirming it's a minimum

        This is the complete picture: the first derivative tells us where extrema are, and the
        second derivative tells us what kind of extrema they are.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Part XI: A Glimpse of Integration

        ### The Inverse Problem

        If differentiation answers "What is the rate of change?", then **integration** answers
        the reverse question: "Given the rate of change, what is the total accumulated quantity?"

        **Examples:**
        - If you know velocity (rate of change of position), integration gives you total distance traveled
        - If you know how fast water flows into a tank, integration tells you how much water accumulated
        - If you know the density of a rod at each point, integration gives you the total mass

        ### The Geometric View: Area Under a Curve

        Geometrically, while the derivative gives us the **slope** of the tangent line, the integral
        gives us the **area** under the curve.

        For a function $f(x) \geq 0$, the integral from $a$ to $b$ represents the area between
        the curve and the x-axis:

        $$\int_a^b f(x) \, dx = \text{area under } f(x) \text{ from } x = a \text{ to } x = b$$

        ### The Riemann Sum: Building Intuition

        How do we find this area? The same way we found derivatives—by taking a limit.

        **The idea:**
        1. Divide the region into thin vertical rectangles
        2. Add up the areas of all the rectangles
        3. Take the limit as the rectangles become infinitely thin

        This sum of rectangle areas is called a **Riemann sum**, named after mathematician
        Bernhard Riemann.

        As the number of rectangles increases (and their width decreases), the sum approaches
        the true area. The limit of this process is the definite integral.

        ### The Fundamental Theorem of Calculus

        Here's the stunning punchline: **differentiation and integration are inverse operations**.

        If $F(x)$ is an antiderivative of $f(x)$ (meaning $F'(x) = f(x)$), then:

        $$\int_a^b f(x) \, dx = F(b) - F(a)$$

        This is the **Fundamental Theorem of Calculus**, perhaps the most important theorem in
        all of mathematics. It connects the two main ideas of calculus (rate of change and
        accumulated quantity) into a unified whole.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Interactive Exploration: Riemann Sums

        Below, you can see this approximation process in action. We're computing
        $\int_0^3 x^2 \, dx$ — the area under the parabola $y = x^2$ from $x = 0$ to $x = 3$.

        Use the slider to change the number of rectangles. Watch how:
        - More rectangles = better approximation
        - The "staircase" shape becomes smoother
        - The computed area converges to the exact value (9.0)
        """
    )
    return


@app.cell
def _(mo):
    rect_slider = mo.ui.slider(
        start=5, stop=100, step=5, value=10,
        label="Number of rectangles:",
        show_value=True,
    )
    return rect_slider,


@app.cell
def _(mo, rect_slider):
    mo.hstack([
        mo.md("**Adjust the approximation:**"),
        rect_slider,
    ])
    return


@app.cell
def _(go, np, rect_slider):
    _n = rect_slider.value
    _a, _b = 0, 3
    _x_curve = np.linspace(_a, _b, 200)
    _y_curve = _x_curve ** 2  # f(x) = x²

    _dx = (_b - _a) / _n
    _x_bars = np.array([_a + i * _dx for i in range(_n)])
    _heights = (_x_bars + _dx / 2) ** 2  # Midpoint rule
    _area = np.sum(_heights * _dx)
    _true_area = _b ** 3 / 3 - _a ** 3 / 3  # ∫x² dx = x³/3

    _fig = go.Figure()

    # Rectangles
    _fig.add_trace(go.Bar(
        x=_x_bars + _dx / 2,
        y=_heights,
        width=_dx * 0.95,
        marker_color='#4ecdc4',
        opacity=0.6,
        name=f'Riemann sum ≈ {_area:.4f}',
    ))

    # Function curve
    _fig.add_trace(go.Scatter(
        x=_x_curve, y=_y_curve,
        mode='lines',
        line={'color': '#00d4ff', 'width': 3},
        name='f(x) = x²',
    ))

    _fig.update_layout(
        paper_bgcolor='#16213e',
        plot_bgcolor='#1a1a2e',
        font={'color': '#eaeaea', 'family': 'JetBrains Mono, monospace'},
        title=f"∫₀³ x² dx: Riemann Sum = {_area:.4f}, Exact = {_true_area:.4f}",
        xaxis={'gridcolor': '#2d3a4f', 'zerolinecolor': '#a0a0a0', 'title': 'x'},
        yaxis={'gridcolor': '#2d3a4f', 'zerolinecolor': '#a0a0a0', 'title': 'y'},
        barmode='overlay',
        showlegend=True,
        legend={'bgcolor': 'rgba(22, 33, 62, 0.8)'},
    )
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        **Try it!** Increase the number of rectangles and watch as:
        - The Riemann sum gets closer to the exact area (9.0)
        - The rectangles fill in the curve more precisely
        - The "staircase" approximation becomes smoother

        With 100 rectangles, we get within 0.01% of the true answer. With infinitely many
        rectangles of infinitesimal width, we get the exact integral.

        **The exact calculation:**

        The antiderivative of $f(x) = x^2$ is $F(x) = \frac{x^3}{3}$ (verify: $F'(x) = x^2$ ✓)

        By the Fundamental Theorem of Calculus:
        $$\begin{aligned}
        \int_0^3 x^2 \, dx &= F(3) - F(0) \\
        &= \frac{3^3}{3} - \frac{0^3}{3} \\
        &= \frac{27}{3} - 0 \\
        &= 9
        \end{aligned}$$

        This is much easier than computing an infinite sum of rectangles!
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Summary

        We've traced the development of one of humanity's greatest intellectual achievements:

        ### The Core Ideas

        1. **The Problem**: How to describe instantaneous rates of change mathematically

        2. **The Solution**: The derivative, defined as a limit:
           $$f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}$$

        3. **The Tools**: Rules that let us compute derivatives quickly:
           - Power rule: $(x^n)' = nx^{n-1}$
           - Chain rule: $(f(g(x)))' = f'(g(x)) \cdot g'(x)$
           - And many others

        4. **The Geometric Meaning**: The derivative is the slope of the tangent line,
           which is the best linear approximation to a function at a point

        5. **Applications**:
           - Physics: velocity is the derivative of position
           - Optimization: maxima and minima occur where the derivative is zero
           - Integration: the inverse operation that finds accumulated quantities

        ### The Big Picture

        Newton and Leibniz gave us not just a mathematical technique, but a new way of thinking
        about the world—a language for describing change itself.

        Before calculus, mathematics could only describe static situations. After calculus,
        mathematics could describe motion, growth, decay, waves, heat flow, electromagnetic
        fields, quantum mechanics, and everything else that changes.

        This is why calculus is the foundation of all modern science and engineering.

        ---

        ## Further Resources

        ### Video Series
        - [3Blue1Brown: Essence of Calculus](https://www.youtube.com/playlist?list=PLZHQObOWTQDMsr9K-rj53DwVRMYO3t5Yr) — Beautiful visual explanations
        - [Khan Academy: Differential Calculus](https://www.khanacademy.org/math/differential-calculus) — Comprehensive course

        ### Primary Sources
        - [Newton's Method of Fluxions (1671)](https://archive.org/details/methodoffluxions00newt)
        - [Leibniz's Nova Methodus (1684)](https://www.maa.org/press/periodicals/convergence/mathematical-treasure-leibnizs-papers-on-calculus-differential-calculus)
        - [Newton's Principia (1687)](https://archive.org/details/mathematicalprin00newtuoft)

        ### Modern Textbooks
        - Stewart, *Calculus: Early Transcendentals* — The standard university textbook
        - Spivak, *Calculus* — Rigorous treatment for the mathematically adventurous
        - Strang, *Calculus* — Free online at MIT OpenCourseWare
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        *"The calculus was the first achievement of modern mathematics, and it is difficult to
        overestimate its importance. I think it defines more unequivocally than anything else the
        inception of modern mathematics, and the system of mathematical analysis, which is its
        logical development, still constitutes the greatest technical advance in exact thinking."*

        — John von Neumann
        """
    )
    return


if __name__ == "__main__":
    app.run()
