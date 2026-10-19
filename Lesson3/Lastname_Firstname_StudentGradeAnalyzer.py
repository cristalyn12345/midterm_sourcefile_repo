
raw_records = [
    "Ana,88,92,90",
    "Ben,70,72,74",
    "Cara,95,91,94",
    "Dan,78,80,76",
    "Ella,85,89,87",
    "Fred,90,85",
    "Gina",
    "Henry,90,eighty,85",
    "Ivy,",
]

PASSING_GRADE = 75

student_scores = {}

for record in raw_records:
    
    fields = record.split(",")

    if len(fields) != 4:
        print(f"Skipped invalid record: {record}")
        continue

    name = fields[0].strip()

    if name == "":
        print(f"Skipped invalid record: {record}")
        continue

    try:
        scores = [int(score) for score in fields[1:]]
    except ValueError:
        print(f"Skipped invalid record: {record}")
        continue

    student_scores[name] = scores


print("\nORGANIZED STUDENT RECORDS")

for name in sorted(student_scores.keys()):
    print(f"{name}: {student_scores[name]}")


ranking = []

passed_count = 0
failed_count = 0
sum_of_averages = 0

for name, scores in student_scores.items():
    if len(scores) == 0:
        print(f"Skipped student with no scores: {name}")
        continue

    total = sum(scores)
    average = total / len(scores)
    highest_score = max(scores)
    lowest_score = min(scores)

    if average >= PASSING_GRADE:
        remark = "Passed"
        passed_count += 1
    else:
        remark = "Failed"
        failed_count += 1

    sum_of_averages += average

    ranking.append((average, name, highest_score, lowest_score, remark))


ranking.sort(reverse=True)

print("\nSTUDENT GRADE REPORT")
print(f"{'Rank':<6}{'Name':<10}{'Average':<10}{'Highest':<10}{'Lowest':<10}{'Remark'}")

for rank, (average, name, highest, lowest, remark) in enumerate(ranking, start=1):
    print(f"{rank:<6}{name:<10}{round(average, 2):<10}{highest:<10}{lowest:<10}{remark}")


print("\nCLASS SUMMARY")

if len(ranking) > 0:
    class_average = sum_of_averages / len(ranking)
    highest_student = ranking[0]   
    lowest_student = ranking[-1]   
else:
    class_average = 0
    highest_student = None
    lowest_student = None

print(f"Number of Students: {len(ranking)}")
print(f"Passed: {passed_count}")
print(f"Failed: {failed_count}")
print(f"Class Average: {round(class_average, 2)}")

if highest_student:
    print(f"Highest: {highest_student[1]} - {round(highest_student[0], 2)}")
if lowest_student:
    print(f"Lowest: {lowest_student[1]} - {round(lowest_student[0], 2)}")