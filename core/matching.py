def calculate_match_score(preferences_a, preferences_b):
    score = 0

    # 1. Location
    if (
        preferences_a.preferred_location.strip().lower()
        == preferences_b.preferred_location.strip().lower()
    ):
        score += 25

    # 2. Budget
    budget_difference = abs(
        float(preferences_a.budget_max)
        - float(preferences_b.budget_max)
    )

    if budget_difference <= 2000:
        score += 25

    # 3. Study habits
    if (
        preferences_a.study_habits.strip().lower()
        == preferences_b.study_habits.strip().lower()
    ):
        score += 20

    # 4. Cleanliness
    cleanliness_difference = abs(
        preferences_a.cleanliness_level
        - preferences_b.cleanliness_level
    )

    if cleanliness_difference <= 1:
        score += 15

    # 5. Smoking
    if preferences_a.smoking_allowed == preferences_b.smoking_allowed:
        score += 10

    # 6. Guests
    if preferences_a.guests_allowed == preferences_b.guests_allowed:
        score += 5

    return score