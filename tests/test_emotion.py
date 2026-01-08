from backend.app.services.emotion import detect_emotion, get_emotion_vector


def test_detect_happy():
    r = detect_emotion("I am so happy today!")
    assert r["label"] == "happy"
    v = get_emotion_vector(r)
    assert "valence" in v and "arousal" in v


def test_detect_sad():
    r = detect_emotion("I feel very sad and down.")
    assert r["label"] == "sad"


def test_detect_neutral():
    r = detect_emotion("This is a statement without emotion")
    assert r["label"] == "neutral"
