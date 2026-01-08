from backend.app.services.emotion import detect_emotion
from backend.app.services.intent import detect_intent
from backend.app.services.decision import choose_response


def test_crying_empathy():
    e = detect_emotion("I am crying a lot")
    assert e['label'] == 'sad'
    resp = choose_response({'intent': 'unknown'}, e, {})
    assert "sorry" in resp.lower() or "talk about" in resp.lower()


def test_suggestion_for_question():
    intent = detect_intent("what should i do to feel nice")
    assert intent['intent'] == 'ask_suggestion'
    emotion = detect_emotion("what should i do to feel nice")
    resp = choose_response(intent, emotion, {})
    assert "ideas" in resp.lower() or "suggestion" in resp.lower()


def test_sad_suggestion_combined():
    intent = detect_intent("what should i do to feel better")
    emotion = detect_emotion("i am crying")
    resp = choose_response(intent, emotion, {})
    assert "you're feeling down" in resp.lower() or "sorry" in resp.lower()
