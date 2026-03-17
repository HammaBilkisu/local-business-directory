questions = [
    {
        "question": "What is the capital of France?",
        "options": ["A) Berlin", "B) Madrid", "C) Paris", "D) Rome"],
        "correct_answer": "C"
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["A) Venus", "B) Mars", "C) Jupiter", "D) Saturn"],
        "correct_answer": "B"
    },
    {
        "question": "What is 12 x 12?",
        "options": ["A) 132", "B) 144", "C) 124", "D) 156"],
        "correct_answer": "B"
    },
    {
        "question": "Who wrote 'Romeo and Juliet'?",
        "options": ["A) Charles Dickens", "B) Jane Austen", "C) Mark Twain", "D) William Shakespeare"],
        "correct_answer": "D"
    },
    {
        "question": "What is the chemical symbol for water?",
        "options": ["A) O2", "B) CO2", "C) H2O", "D) NaCl"],
        "correct_answer": "C"
    }
]


def calculate_result(score, total):
    percentage = (score / total) * 100
    if percentage >= 60:
        status = "PASS"
    else:
        status = "FAIL"
    return percentage, status


def run_quiz():
    print("=" * 40)
    print("        Welcome to the CLI Quiz!")
    print("=" * 40)
    print(f"You will be asked {len(questions)} questions.")
    print("Enter the letter of your answer (A, B, C, or D).\n")

    score = 0

    for i, q in enumerate(questions, start=1):
        print(f"Question {i}: {q['question']}")
        for option in q["options"]:
            print(f"  {option}")

        user_answer = input("Your answer: ").strip().upper()

        if user_answer == q["correct_answer"]:
            print("Correct!\n")
            score += 1
        else:
            print(f"Wrong! The correct answer was {q['correct_answer']}.\n")

    print("=" * 40)
    print("           Quiz Complete!")
    print("=" * 40)
    percentage, status = calculate_result(score, len(questions))
    print(f"Score: {score}/{len(questions)}")
    print(f"Percentage: {percentage:.1f}%")
    print(f"Result: {status}")
    print("=" * 40)


run_quiz()
