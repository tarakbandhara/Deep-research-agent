import asyncio
import chainlit as cl
from dotenv import load_dotenv

from research_manager import ResearchManager


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv(override=True)


# ============================================================
# HOME SCREEN STARTER BUTTON
# ============================================================

@cl.set_starters
async def set_starters():

    return [
        cl.Starter(
            label="📚 Find the latest information about Ai Agents",
            message="Find the latest reliable information about: Ai Agents",
        ),
    ]


# ============================================================
# RESEARCH PROGRESS
# ============================================================

def progress_message(
    stage: str,
    dots: str = "...",
    active_dot: str = "●",
) -> str:

    if stage == "planning":
        return (
            f"{active_dot} **Planning{dots}**"
        )

    if stage == "searching":
        return (
            "✓ **Planning**\n"
            f"{active_dot} **Searching{dots}**"
        )

    if stage == "writing":
        return (
            "✓ **Planning**\n"
            "✓ **Searching**\n"
            f"{active_dot} **Writing{dots}**"
        )

    if stage == "finalizing":
        return (
            "✓ **Planning**\n"
            "✓ **Searching**\n"
            "✓ **Writing**\n"
            f"{active_dot} **Finalizing{dots}**"
        )

    if stage == "complete":
        return (
            "✓ **Research complete**"
        )

    return (
        f"{active_dot} **Planning{dots}**"
    )


# ============================================================
# RATE LIMIT DETECTION
# ============================================================

def is_rate_limit_error(error: Exception) -> bool:

    current = error

    while current is not None:

        # ----------------------------------------------------
        # Exception class name
        # ----------------------------------------------------

        class_name = current.__class__.__name__.lower()

        if "ratelimit" in class_name:
            return True

        if "rate_limit" in class_name:
            return True

        # ----------------------------------------------------
        # HTTP status code
        # ----------------------------------------------------

        status_code = getattr(
            current,
            "status_code",
            None,
        )

        if status_code == 429:
            return True

        # ----------------------------------------------------
        # Response status code
        # ----------------------------------------------------

        response = getattr(
            current,
            "response",
            None,
        )

        if response is not None:

            response_status = getattr(
                response,
                "status_code",
                None,
            )

            if response_status == 429:
                return True

        # ----------------------------------------------------
        # Error message
        # ----------------------------------------------------

        error_text = str(current).lower()

        rate_limit_phrases = [
            "rate limit",
            "rate-limit",
            "rate_limit",
            "too many requests",
            "429",
            "requests per minute",
            "tokens per minute",
            "quota exceeded",
        ]

        if any(
            phrase in error_text
            for phrase in rate_limit_phrases
        ):
            return True

        # ----------------------------------------------------
        # Follow exception chain
        # ----------------------------------------------------

        next_error = (
            getattr(current, "__cause__", None)
            or getattr(current, "__context__", None)
        )

        if next_error is current:
            break

        current = next_error

    return False


# ============================================================
# RATE LIMIT MESSAGE
# ============================================================

def rate_limit_message(error: Exception) -> str:

    message = (
        "⚠️ **Rate limit reached**\n\n"
        "The research could not continue because the AI service "
        "rate limit was reached.\n\n"
        "Please wait a moment and try again."
    )

    # --------------------------------------------------------
    # Try to find Retry-After information
    # --------------------------------------------------------

    retry_after = getattr(
        error,
        "retry_after",
        None,
    )

    if retry_after is None:

        response = getattr(
            error,
            "response",
            None,
        )

        if response is not None:

            headers = getattr(
                response,
                "headers",
                None,
            )

            if headers:

                retry_after = (
                    headers.get("retry-after")
                    or headers.get("Retry-After")
                )

    if retry_after:

        message += (
            f"\n\n**Retry-After:** `{retry_after}`"
        )

    return message


# ============================================================
# GENERAL ERROR MESSAGE
# ============================================================

def general_error_message(error: Exception) -> str:

    return (
        "❌ **Research failed.**\n\n"
        "Something went wrong while running the research process.\n\n"
        f"`{error}`"
    )


# ============================================================
# ACTIVE PROGRESS ANIMATION
# ============================================================

async def animate_progress(
    status: cl.Message,
    stage: str,
    stop_event: asyncio.Event,
):
    """
    Animate both:

    1. The active dot:
       ● → ○ → ● → ○

    2. The trailing dots:
       . → .. → ...

    This creates a subtle live-process effect while the
    actual research is running.
    """

    dot_states = [
        ".",
        "..",
        "...",
    ]

    active_dots = [
        "●",
        "○",
    ]

    dot_index = 0
    blink_index = 0

    while not stop_event.is_set():

        status.content = progress_message(
            stage,
            dot_states[dot_index],
            active_dots[blink_index],
        )

        await status.update()

        # ----------------------------------------------------
        # Advance animation
        # ----------------------------------------------------

        dot_index = (
            dot_index + 1
        ) % len(dot_states)

        blink_index = (
            blink_index + 1
        ) % len(active_dots)

        # ----------------------------------------------------
        # Wait before next frame
        # ----------------------------------------------------

        try:

            await asyncio.wait_for(
                stop_event.wait(),
                timeout=0.45,
            )

        except asyncio.TimeoutError:

            pass


# ============================================================
# MESSAGE HANDLER
# ============================================================

@cl.on_message
async def on_message(message: cl.Message):

    query = message.content.strip()

    # ========================================================
    # EMPTY MESSAGE
    # ========================================================

    if not query:

        await cl.Message(
            content="Please enter a question to research."
        ).send()

        return

    # ========================================================
    # RESEARCH MANAGER
    # ========================================================

    manager = ResearchManager()

    final_report = None

    # ========================================================
    # STATUS MESSAGE
    # ========================================================

    status = cl.Message(
        content=progress_message(
            "planning",
            ".",
            "●",
        )
    )

    await status.send()

    # ========================================================
    # ANIMATION CONTROL
    # ========================================================

    animation_stop = asyncio.Event()

    current_stage = "planning"

    animation_task = asyncio.create_task(
        animate_progress(
            status,
            current_stage,
            animation_stop,
        )
    )

    try:

        # ====================================================
        # RUN REAL RESEARCH
        # ====================================================

        async for update in manager.run(query):

            # ------------------------------------------------
            # STEP 1 — PLANNING
            # ------------------------------------------------

            if update.startswith("Starting research"):

                current_stage = "planning"

                animation_stop.set()

                await animation_task

                animation_stop = asyncio.Event()

                animation_task = asyncio.create_task(
                    animate_progress(
                        status,
                        current_stage,
                        animation_stop,
                    )
                )

            # ------------------------------------------------
            # STEP 2 — SEARCHING
            # ------------------------------------------------

            elif update.startswith("Searches planned"):

                current_stage = "searching"

                animation_stop.set()

                await animation_task

                animation_stop = asyncio.Event()

                animation_task = asyncio.create_task(
                    animate_progress(
                        status,
                        current_stage,
                        animation_stop,
                    )
                )

            # ------------------------------------------------
            # STEP 3 — WRITING
            # ------------------------------------------------

            elif update == "Searches complete, writing report...":

                current_stage = "writing"

                animation_stop.set()

                await animation_task

                animation_stop = asyncio.Event()

                animation_task = asyncio.create_task(
                    animate_progress(
                        status,
                        current_stage,
                        animation_stop,
                    )
                )

            # ------------------------------------------------
            # STEP 4 — FINALIZING
            # ------------------------------------------------

            elif update == "Report written":

                current_stage = "finalizing"

                animation_stop.set()

                await animation_task

                animation_stop = asyncio.Event()

                animation_task = asyncio.create_task(
                    animate_progress(
                        status,
                        current_stage,
                        animation_stop,
                    )
                )

            # ------------------------------------------------
            # STEP 5 — COMPLETE
            # ------------------------------------------------

            elif update == "Research complete":

                animation_stop.set()

                await animation_task

                status.content = progress_message(
                    "complete"
                )

                await status.update()

            # ------------------------------------------------
            # FINAL REPORT
            # ------------------------------------------------

            else:

                final_report = update

        # ====================================================
        # STOP ANIMATION
        # ====================================================

        animation_stop.set()

        if not animation_task.done():

            await animation_task

        # ====================================================
        # SEND FINAL REPORT
        # ====================================================

        if final_report:

            await cl.Message(
                content=final_report
            ).send()

    # ========================================================
    # ERROR HANDLING
    # ========================================================

    except Exception as error:

        print("Research failed:")
        print(repr(error))

        # ----------------------------------------------------
        # STOP ANIMATION
        # ----------------------------------------------------

        animation_stop.set()

        if not animation_task.done():

            await animation_task

        # ----------------------------------------------------
        # RATE LIMIT
        # ----------------------------------------------------

        if is_rate_limit_error(error):

            status.content = rate_limit_message(
                error
            )

            await status.update()

            return

        # ----------------------------------------------------
        # OTHER ERROR
        # ----------------------------------------------------

        status.content = general_error_message(
            error
        )

        await status.update()