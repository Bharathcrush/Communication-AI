# ============================================================
# COMMUNICATION AI - SPEECH ANALYZER
# ============================================================
#
# Analyzes transcribed speech for:
# - Pauses and silences
# - Hesitations and filler words
# - Grammar errors
# - Fluency (words per minute)
# - Overall speech score out of 10
# ============================================================

import re


# ============================================================
# FILLER WORDS
# ============================================================

FILLER_WORDS = [
    "um", "uh", "umm", "uhh", "ummm",
    "er", "err", "ah", "ahh",
    "like", "basically", "actually",
    "you know", "i mean", "sort of",
    "kind of", "right", "okay so",
    "well", "so yeah", "yeah"
]


# ============================================================
# MAIN ANALYSIS FUNCTION
# ============================================================

def analyze_speech(
    transcript_text,
    words_with_timestamps,
    session_duration
):
    """
    Analyze speech from a transcription result.

    Parameters:
        transcript_text: The full transcript string
        words_with_timestamps: List of dicts with
            word, start, end times
        session_duration: Total session time in seconds

    Returns:
        Dictionary with all speech analysis results
        and a score out of 10
    """

    # --------------------------------------------------------
    # Handle empty input
    # --------------------------------------------------------

    if (
        not transcript_text
        or not transcript_text.strip()
    ):

        return _empty_result()

    # --------------------------------------------------------
    # Basic stats
    # --------------------------------------------------------

    all_words = transcript_text.split()
    word_count = len(all_words)

    if word_count == 0:

        return _empty_result()

    # --------------------------------------------------------
    # Run all analyses
    # --------------------------------------------------------

    pause_analysis = _analyze_pauses(
        words_with_timestamps,
        session_duration
    )

    filler_analysis = _analyze_fillers(
        transcript_text,
        word_count
    )

    repetition_analysis = _analyze_repetitions(
        all_words
    )

    grammar_analysis = _analyze_grammar(
        transcript_text
    )

    fluency_analysis = _analyze_fluency(
        word_count,
        session_duration,
        pause_analysis,
        filler_analysis,
        words_with_timestamps
    )

    # --------------------------------------------------------
    # Calculate speech score out of 10
    # --------------------------------------------------------

    speech_score = _calculate_speech_score(
        fluency_analysis,
        grammar_analysis,
        pause_analysis,
        filler_analysis,
        repetition_analysis,
        word_count,
        session_duration
    )

    # --------------------------------------------------------
    # Generate feedback
    # --------------------------------------------------------

    speech_feedback = _generate_speech_feedback(
        speech_score,
        fluency_analysis,
        grammar_analysis,
        pause_analysis,
        filler_analysis,
        repetition_analysis
    )

    # --------------------------------------------------------
    # Full result
    # --------------------------------------------------------

    result = {

        "transcript": transcript_text,

        "word_count": word_count,

        "speech_score": speech_score,

        "fluency": fluency_analysis,

        "grammar": grammar_analysis,

        "pauses": pause_analysis,

        "fillers": filler_analysis,

        "repetitions": repetition_analysis,

        "feedback": speech_feedback
    }

    # --------------------------------------------------------
    # Print to console
    # --------------------------------------------------------

    _print_analysis(result)

    return result


# ============================================================
# PAUSE ANALYSIS
# ============================================================

def _analyze_pauses(
    words_with_timestamps,
    session_duration
):
    """
    Detect pauses between words using timestamps.
    """

    pauses = []
    long_pauses = []
    total_silence = 0.0

    if (
        not words_with_timestamps
        or len(words_with_timestamps) < 2
    ):

        return {
            "total_pauses": 0,
            "long_pauses": 0,
            "medium_pauses": 0,
            "pause_list": [],
            "long_pause_list": [],
            "total_silence_seconds": 0.0,
            "silence_ratio": 0.0,
            "pauses_per_minute": 0.0
        }

    # Check gap between each consecutive word
    for i in range(
        1,
        len(words_with_timestamps)
    ):

        prev_end = words_with_timestamps[
            i - 1
        ].get("end", 0.0)

        curr_start = words_with_timestamps[
            i
        ].get("start", 0.0)

        gap = curr_start - prev_end

        if gap < 0:
            gap = 0

        if gap >= 1.0:

            pause_info = {
                "after_word": words_with_timestamps[
                    i - 1
                ].get("word", ""),
                "before_word": words_with_timestamps[
                    i
                ].get("word", ""),
                "duration": round(gap, 1),
                "timestamp": round(prev_end, 1)
            }

            pauses.append(pause_info)
            total_silence += gap

            if gap >= 3.0:

                long_pauses.append(pause_info)

    # First word delay
    if words_with_timestamps:

        first_start = words_with_timestamps[
            0
        ].get("start", 0.0)

        if first_start >= 2.0:

            total_silence += first_start

    # Medium pauses: 1.5 to 3 seconds
    medium_pauses = [
        p for p in pauses
        if 1.5 <= p["duration"] < 3.0
    ]

    # Silence ratio
    speaking_duration = max(
        session_duration,
        1
    )

    silence_ratio = round(
        total_silence / speaking_duration,
        2
    )

    # Pauses per minute
    minutes = max(
        session_duration / 60.0,
        0.1
    )

    pauses_per_minute = round(
        len(pauses) / minutes,
        1
    )

    return {
        "total_pauses": len(pauses),
        "long_pauses": len(long_pauses),
        "medium_pauses": len(medium_pauses),
        "pause_list": pauses,
        "long_pause_list": long_pauses,
        "total_silence_seconds": round(
            total_silence, 1
        ),
        "silence_ratio": silence_ratio,
        "pauses_per_minute": pauses_per_minute
    }


# ============================================================
# FILLER WORD ANALYSIS
# ============================================================

def _analyze_fillers(
    transcript_text,
    word_count
):
    """
    Detect filler words in the transcript.
    """

    text_lower = transcript_text.lower()
    found_fillers = []

    for filler in FILLER_WORDS:

        # Count occurrences
        pattern = r'\b' + re.escape(filler) + r'\b'

        matches = re.findall(
            pattern,
            text_lower
        )

        if matches:

            found_fillers.append({
                "word": filler,
                "count": len(matches)
            })

    total_fillers = sum(
        f["count"] for f in found_fillers
    )

    filler_ratio = round(
        total_fillers / max(word_count, 1),
        3
    )

    return {
        "total_fillers": total_fillers,
        "filler_list": found_fillers,
        "filler_ratio": filler_ratio
    }


# ============================================================
# REPETITION / STUTTERING ANALYSIS
# ============================================================

def _analyze_repetitions(all_words):
    """
    Detect repeated consecutive words (stuttering).
    Example: "I I I" or "the the"
    """

    repetitions = []
    i = 0

    while i < len(all_words) - 1:

        word = all_words[i].lower().strip(
            ".,!?;:"
        )

        next_word = all_words[i + 1].lower().strip(
            ".,!?;:"
        )

        if (
            word == next_word
            and len(word) > 0
        ):

            count = 2
            j = i + 2

            while (
                j < len(all_words)
                and all_words[j].lower().strip(
                    ".,!?;:"
                ) == word
            ):

                count += 1
                j += 1

            repetitions.append({
                "word": word,
                "times": count,
                "position": i
            })

            i = j

        else:

            i += 1

    return {
        "total_repetitions": len(repetitions),
        "repetition_list": repetitions
    }


# ============================================================
# GRAMMAR ANALYSIS
# ============================================================

def _analyze_grammar(transcript_text):
    """
    Check grammar using language_tool_python.
    """

    try:

        import language_tool_python

        tool = language_tool_python.LanguageTool(
            "en-US"
        )

        matches = tool.check(
            transcript_text
        )

        errors = []

        for match in matches:

            # Skip certain categories
            if match.ruleId in [
                "UPPERCASE_SENTENCE_START",
                "MORFOLOGIK_RULE_EN_US"
            ]:
                continue

            errors.append({
                "message": match.message,
                "context": match.context,
                "suggestion": (
                    match.replacements[0]
                    if match.replacements
                    else ""
                ),
                "category": match.category,
                "rule": match.ruleId
            })

        tool.close()

        error_count = len(errors)

        return {
            "total_errors": error_count,
            "error_list": errors[:10],
            "grammar_available": True
        }

    except Exception as e:

        print(
            f"Grammar check not available: {e}"
        )

        return {
            "total_errors": 0,
            "error_list": [],
            "grammar_available": False
        }


# ============================================================
# FLUENCY ANALYSIS
# ============================================================

def _analyze_fluency(
    word_count,
    session_duration,
    pause_analysis,
    filler_analysis,
    words_with_timestamps
):
    """
    Calculate fluency metrics.
    """

    # Words per minute
    minutes = max(
        session_duration / 60.0,
        0.1
    )

    wpm = round(
        word_count / minutes,
        1
    )

    # Speaking time (total - silence)
    silence = pause_analysis.get(
        "total_silence_seconds",
        0.0
    )

    speaking_time = max(
        session_duration - silence,
        1
    )

    speaking_ratio = round(
        speaking_time / max(
            session_duration, 1
        ),
        2
    )

    # Effective WPM (based on speaking time only)
    speaking_minutes = max(
        speaking_time / 60.0,
        0.1
    )

    effective_wpm = round(
        word_count / speaking_minutes,
        1
    )

    # WPM rating
    if 120 <= effective_wpm <= 160:
        wpm_rating = "Good"
    elif 100 <= effective_wpm < 120:
        wpm_rating = "Slightly Slow"
    elif 160 < effective_wpm <= 190:
        wpm_rating = "Slightly Fast"
    elif effective_wpm < 100:
        wpm_rating = "Too Slow"
    else:
        wpm_rating = "Too Fast"

    # Hesitation indicators from timestamps
    hesitation_words = 0

    if words_with_timestamps:

        for w in words_with_timestamps:

            word_duration = (
                w.get("end", 0)
                - w.get("start", 0)
            )

            # A single word taking > 1.5 sec
            # suggests elongation / thinking
            if word_duration > 1.5:

                hesitation_words += 1

    return {
        "wpm": wpm,
        "effective_wpm": effective_wpm,
        "wpm_rating": wpm_rating,
        "speaking_time": round(
            speaking_time, 1
        ),
        "speaking_ratio": speaking_ratio,
        "hesitation_words": hesitation_words
    }


# ============================================================
# SPEECH SCORE CALCULATION (OUT OF 10)
# ============================================================

def _calculate_speech_score(
    fluency,
    grammar,
    pauses,
    fillers,
    repetitions,
    word_count,
    session_duration
):
    """
    Calculate overall speech score out of 10.

    Formula:
        Fluency     = 3.0 points max
        Grammar     = 2.5 points max
        Confidence  = 2.0 points max
        Clarity     = 2.5 points max
        TOTAL       = 10.0 points
    """

    # --------------------------------------------------------
    # 1. FLUENCY SCORE (3.0 max)
    # --------------------------------------------------------

    # WPM component (1.5 max)
    ewpm = fluency.get("effective_wpm", 0)

    if 120 <= ewpm <= 160:
        wpm_score = 1.5
    elif 100 <= ewpm < 120 or 160 < ewpm <= 190:
        wpm_score = 1.0
    elif 80 <= ewpm < 100 or 190 < ewpm <= 210:
        wpm_score = 0.5
    else:
        wpm_score = 0.2

    # Filler word component (1.5 max)
    filler_ratio = fillers.get(
        "filler_ratio", 0
    )

    if filler_ratio <= 0.02:
        filler_score = 1.5
    elif filler_ratio <= 0.05:
        filler_score = 1.0
    elif filler_ratio <= 0.10:
        filler_score = 0.5
    else:
        filler_score = 0.2

    fluency_score = round(
        wpm_score + filler_score,
        1
    )

    # --------------------------------------------------------
    # 2. GRAMMAR SCORE (2.5 max)
    # --------------------------------------------------------

    grammar_errors = grammar.get(
        "total_errors", 0
    )

    if not grammar.get("grammar_available", False):

        # If grammar tool not available,
        # give a neutral score
        grammar_score = 1.5

    else:

        error_per_100 = (
            grammar_errors /
            max(word_count / 100, 0.5)
        )

        if error_per_100 <= 1:
            grammar_score = 2.5
        elif error_per_100 <= 3:
            grammar_score = 2.0
        elif error_per_100 <= 5:
            grammar_score = 1.5
        elif error_per_100 <= 8:
            grammar_score = 1.0
        else:
            grammar_score = 0.5

    # --------------------------------------------------------
    # 3. CONFIDENCE SCORE (2.0 max)
    # --------------------------------------------------------

    # Based on pauses and hesitations
    long_pauses = pauses.get(
        "long_pauses", 0
    )

    total_pauses = pauses.get(
        "total_pauses", 0
    )

    repetition_count = repetitions.get(
        "total_repetitions", 0
    )

    hesitation_words = fluency.get(
        "hesitation_words", 0
    )

    confidence_deductions = (
        long_pauses * 0.3
        + min(total_pauses, 10) * 0.05
        + repetition_count * 0.2
        + hesitation_words * 0.1
    )

    confidence_score = round(
        max(
            0.2,
            2.0 - confidence_deductions
        ),
        1
    )

    # --------------------------------------------------------
    # 4. CLARITY SCORE (2.5 max)
    # --------------------------------------------------------

    # Based on speaking ratio and word count
    speaking_ratio = fluency.get(
        "speaking_ratio", 0
    )

    silence_ratio = pauses.get(
        "silence_ratio", 0
    )

    if speaking_ratio >= 0.75:
        clarity_base = 2.5
    elif speaking_ratio >= 0.60:
        clarity_base = 2.0
    elif speaking_ratio >= 0.45:
        clarity_base = 1.5
    elif speaking_ratio >= 0.30:
        clarity_base = 1.0
    else:
        clarity_base = 0.5

    # Penalize if very few words spoken
    if word_count < 10 and session_duration > 10:
        clarity_base = max(
            0.5,
            clarity_base - 1.0
        )

    clarity_score = round(
        clarity_base,
        1
    )

    # --------------------------------------------------------
    # TOTAL SCORE
    # --------------------------------------------------------

    total = round(
        fluency_score
        + grammar_score
        + confidence_score
        + clarity_score,
        1
    )

    # Clamp to 0-10
    total = max(0.0, min(10.0, total))

    return {
        "total": total,
        "fluency": fluency_score,
        "grammar": grammar_score,
        "confidence": confidence_score,
        "clarity": clarity_score
    }


# ============================================================
# SPEECH FEEDBACK GENERATOR
# ============================================================

def _generate_speech_feedback(
    scores,
    fluency,
    grammar,
    pauses,
    fillers,
    repetitions
):
    """
    Generate human-readable speech feedback.
    """

    strengths = []
    improvements = []
    suggestions = []

    total = scores.get("total", 0)

    # --------------------------------------------------------
    # Fluency feedback
    # --------------------------------------------------------

    wpm_rating = fluency.get(
        "wpm_rating", ""
    )

    ewpm = fluency.get("effective_wpm", 0)

    if wpm_rating == "Good":

        strengths.append(
            f"Good speaking pace ({ewpm} words/min)."
        )

    elif "Slow" in wpm_rating:

        improvements.append(
            f"Speaking pace is slow ({ewpm} words/min)."
        )

        suggestions.append(
            "Try to speak more naturally "
            "without long pauses between ideas."
        )

    elif "Fast" in wpm_rating:

        improvements.append(
            f"Speaking pace is too fast ({ewpm} words/min)."
        )

        suggestions.append(
            "Slow down slightly so your words "
            "are clearer and easier to follow."
        )

    # --------------------------------------------------------
    # Filler word feedback
    # --------------------------------------------------------

    total_fillers = fillers.get(
        "total_fillers", 0
    )

    if total_fillers == 0:

        strengths.append(
            "No filler words detected."
        )

    elif total_fillers <= 3:

        strengths.append(
            "Very few filler words used."
        )

    else:

        filler_list = fillers.get(
            "filler_list", []
        )

        top_fillers = sorted(
            filler_list,
            key=lambda x: x["count"],
            reverse=True
        )[:3]

        filler_names = ", ".join(
            f"'{f['word']}' ({f['count']}x)"
            for f in top_fillers
        )

        improvements.append(
            f"Too many filler words: {filler_names}."
        )

        suggestions.append(
            "Practice speaking without filler words "
            "like 'um', 'uh', and 'like'."
        )

    # --------------------------------------------------------
    # Pause feedback
    # --------------------------------------------------------

    long_pauses = pauses.get(
        "long_pauses", 0
    )

    long_pause_list = pauses.get(
        "long_pause_list", []
    )

    if long_pauses == 0:

        strengths.append(
            "No long silences during speech."
        )

    else:

        pause_details = []

        for p in long_pause_list[:3]:

            pause_details.append(
                f"{p['duration']}s pause after "
                f"'{p['after_word']}'"
            )

        pause_text = "; ".join(
            pause_details
        )

        improvements.append(
            f"{long_pauses} long silence(s) detected: "
            f"{pause_text}."
        )

        suggestions.append(
            "Prepare your thoughts beforehand "
            "to reduce long pauses while speaking."
        )

    # --------------------------------------------------------
    # Repetition / stuttering feedback
    # --------------------------------------------------------

    rep_count = repetitions.get(
        "total_repetitions", 0
    )

    if rep_count > 0:

        rep_list = repetitions.get(
            "repetition_list", []
        )

        rep_words = ", ".join(
            f"'{r['word']}' ({r['times']}x)"
            for r in rep_list[:3]
        )

        improvements.append(
            f"Word repetition detected: {rep_words}."
        )

        suggestions.append(
            "Take a breath instead of repeating "
            "words when you need time to think."
        )

    # --------------------------------------------------------
    # Grammar feedback
    # --------------------------------------------------------

    grammar_errors = grammar.get(
        "total_errors", 0
    )

    if grammar.get("grammar_available", False):

        if grammar_errors == 0:

            strengths.append(
                "No grammar issues detected."
            )

        elif grammar_errors <= 3:

            improvements.append(
                f"{grammar_errors} minor grammar "
                f"issue(s) found."
            )

            suggestions.append(
                "Review basic grammar rules to "
                "improve sentence structure."
            )

        else:

            error_list = grammar.get(
                "error_list", []
            )

            sample_errors = []

            for err in error_list[:2]:
                if err.get("suggestion"):
                    sample_errors.append(
                        err["message"]
                    )

            if sample_errors:

                improvements.append(
                    f"{grammar_errors} grammar errors found. "
                    f"Example: {sample_errors[0]}"
                )

            else:

                improvements.append(
                    f"{grammar_errors} grammar errors found."
                )

            suggestions.append(
                "You need to improve your grammar. "
                "Practice forming complete and "
                "correct sentences."
            )

    # --------------------------------------------------------
    # Speaking ratio feedback
    # --------------------------------------------------------

    speaking_ratio = fluency.get(
        "speaking_ratio", 0
    )

    if speaking_ratio >= 0.75:

        strengths.append(
            "Good speaking confidence with "
            "minimal silence."
        )

    elif speaking_ratio < 0.50:

        improvements.append(
            "More than half the session was silent."
        )

        suggestions.append(
            "Need to improve proficiency. "
            "Try to speak more continuously "
            "and express your thoughts clearly."
        )

    # --------------------------------------------------------
    # Overall speech summary
    # --------------------------------------------------------

    if total >= 8.0:

        summary = (
            "Excellent speech performance. "
            "Clear, fluent, and well-structured delivery."
        )

    elif total >= 6.0:

        summary = (
            "Good speech performance. "
            "Some areas can be refined for "
            "a more polished delivery."
        )

    elif total >= 4.0:

        summary = (
            "Average speech performance. "
            "Focus on reducing pauses, filler words, "
            "and improving grammar."
        )

    else:

        summary = (
            "Speech needs significant improvement. "
            "Practice speaking clearly, reducing "
            "long silences, and using proper grammar."
        )

    return {
        "summary": summary,
        "strengths": strengths,
        "improvements": improvements,
        "suggestions": suggestions
    }


# ============================================================
# EMPTY RESULT
# ============================================================

def _empty_result():
    """
    Return a default result when no speech is detected.
    """

    return {

        "transcript": "",

        "word_count": 0,

        "speech_score": {
            "total": 0.0,
            "fluency": 0.0,
            "grammar": 0.0,
            "confidence": 0.0,
            "clarity": 0.0
        },

        "fluency": {
            "wpm": 0,
            "effective_wpm": 0,
            "wpm_rating": "No Speech",
            "speaking_time": 0,
            "speaking_ratio": 0,
            "hesitation_words": 0
        },

        "grammar": {
            "total_errors": 0,
            "error_list": [],
            "grammar_available": False
        },

        "pauses": {
            "total_pauses": 0,
            "long_pauses": 0,
            "medium_pauses": 0,
            "pause_list": [],
            "long_pause_list": [],
            "total_silence_seconds": 0,
            "silence_ratio": 0,
            "pauses_per_minute": 0
        },

        "fillers": {
            "total_fillers": 0,
            "filler_list": [],
            "filler_ratio": 0
        },

        "repetitions": {
            "total_repetitions": 0,
            "repetition_list": []
        },

        "feedback": {
            "summary": "No speech was detected during "
                       "this session.",
            "strengths": [],
            "improvements": [
                "No speech was captured."
            ],
            "suggestions": [
                "Speak clearly into your microphone "
                "during the evaluation."
            ]
        }
    }


# ============================================================
# CONSOLE OUTPUT
# ============================================================

def _print_analysis(result):
    """
    Print speech analysis to console.
    """

    scores = result.get("speech_score", {})
    fluency = result.get("fluency", {})
    pauses = result.get("pauses", {})
    fillers = result.get("fillers", {})
    grammar = result.get("grammar", {})

    print()
    print("=" * 50)
    print("    SPEECH ANALYSIS RESULTS")
    print("=" * 50)

    print(
        f"Words spoken     : "
        f"{result.get('word_count', 0)}"
    )

    print(
        f"Speaking pace    : "
        f"{fluency.get('effective_wpm', 0)} WPM "
        f"({fluency.get('wpm_rating', '')})"
    )

    print(
        f"Speaking time    : "
        f"{fluency.get('speaking_time', 0)}s"
    )

    print(
        f"Pauses detected  : "
        f"{pauses.get('total_pauses', 0)} "
        f"(long: {pauses.get('long_pauses', 0)})"
    )

    print(
        f"Filler words     : "
        f"{fillers.get('total_fillers', 0)}"
    )

    print(
        f"Grammar errors   : "
        f"{grammar.get('total_errors', 0)}"
    )

    print("-" * 50)

    print(
        f"Speech Score     : "
        f"{scores.get('total', 0)}/10"
    )

    print(
        f"  Fluency        : "
        f"{scores.get('fluency', 0)}/3.0"
    )

    print(
        f"  Grammar        : "
        f"{scores.get('grammar', 0)}/2.5"
    )

    print(
        f"  Confidence     : "
        f"{scores.get('confidence', 0)}/2.0"
    )

    print(
        f"  Clarity        : "
        f"{scores.get('clarity', 0)}/2.5"
    )

    print("=" * 50)
    print()
