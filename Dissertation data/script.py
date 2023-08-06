import csv

# Dictionary to map text responses to numerical values for SUS calculation
response_mapping = {
    "Strongly Disagree": 1,
    "Disagree": 2,
    "Neutral": 3,
    "Agree": 4,
    "Strongly Agree": 5
}

# Dictionary to store SUS scores for each mode
sus_scores = {
    "Map": [],
    "Map_irritating": [],
    "Map_distracting": [],
    "Map_tired": [],
    "Map_confident": [],
    "Audio based": [],
    "Audio based_irritating": [],
    "Audio based_distracting": [],
    "Audio based_tired": [],
    "Audio based_continuous": [],
    "Electrotactile Discontinuous": [],
    "Electrotactile Discontinuous_irritating": [],
    "Electrotactile Discontinuous_distracting": [],
    "Electrotactile Discontinuous_tired": [],
    "Electrotactile Discontinuous_itchy": [],
    "Electrotactile Continuous": [],
    "Electrotactile Continuous_irritating": [],
    "Electrotactile Continuous_distracting": [],
    "Electrotactile Continuous_tired": [],
    "Electrotactile Continuous_itchy": [],
}
m = {
    "Map": [],
    "Audio based": [],
    "Electrotactile Discontinuous": [],
    "Electrotactile Continuous": []
}
modes = list(m.keys())

yes_no_scores = {
    "Yes": 1,
    "No": 0,
    "Maybe": 1
}


def calculate_sus_score(responses):
    odd = (responses[0] + responses[2] + responses[4] +
           responses[6] + responses[8]) - 5
    even = 25 - (responses[1] + responses[3] +
                 responses[5] + responses[7] + responses[9])
    total = (odd + even) * 2.5
    return total


feedback = {
    "Map": [],
    "Audio based": [],
    "Electrotactile Discontinuous": [],
    "Electrotactile Continuous": []
}
# Read and process the CSV file
csv_filename = "data.csv"
with open(csv_filename, 'r', newline='') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)  # Skip header row

    for row in csv_reader:
        for i in range(4):
            # search for the mode
            mode = modes[i]
            index = row.index(modes[i])
            itchy = 0
            irritating = 0
            distracting = 0
            tired = 0
            continuous = 0

            if mode in sus_scores:  # Check if mode is one of the desired modes
                # Extract the 10 SUS responses
                sus_responses = row[index+1:index+11]
                # Convert to numerical values
                sus_numerical = [response_mapping[response]
                                 for response in sus_responses]
                sus_score = calculate_sus_score(
                    sus_numerical)  # Calculate SUS score
                sus_scores[mode].append(sus_score)
                feedback[mode].append(row[index+18])
                if mode == "Map":
                    irritating = yes_no_scores[row[index+17]]
                    distracting = yes_no_scores[row[index+11]]
                    tired = yes_no_scores[row[index+12]]
                    confidence = yes_no_scores[row[index+15]]
                    sus_scores[mode+"_irritating"].append(irritating)
                    sus_scores[mode+"_distracting"].append(distracting)
                    sus_scores[mode+"_tired"].append(tired)
                    sus_scores[mode+"_confident"].append(confidence)
                elif mode == "Audio based":
                    irritating = yes_no_scores[row[index+17]]
                    distracting = yes_no_scores[row[index+11]]
                    tired = yes_no_scores[row[index+12]]
                    continuous = yes_no_scores[row[index+16]]
                    sus_scores[mode+"_irritating"].append(irritating)
                    sus_scores[mode+"_distracting"].append(distracting)
                    sus_scores[mode+"_tired"].append(tired)
                    sus_scores[mode+"_continuous"].append(continuous)
                elif mode == "Electrotactile Discontinuous":
                    irritating = yes_no_scores[row[index+17]]
                    distracting = yes_no_scores[row[index+11]]
                    tired = yes_no_scores[row[index+12]]
                    itchy = yes_no_scores[row[index+13]]
                    sus_scores[mode+"_irritating"].append(irritating)
                    sus_scores[mode+"_distracting"].append(distracting)
                    sus_scores[mode+"_tired"].append(tired)
                    sus_scores[mode+"_itchy"].append(itchy)
                elif mode == "Electrotactile Continuous":
                    irritating = yes_no_scores[row[index+17]]
                    distracting = yes_no_scores[row[index+11]]
                    tired = yes_no_scores[row[index+12]]
                    itchy = yes_no_scores[row[index+14]]
                    sus_scores[mode+"_irritating"].append(irritating)
                    sus_scores[mode+"_distracting"].append(distracting)
                    sus_scores[mode+"_tired"].append(tired)
                    sus_scores[mode+"_itchy"].append(itchy)
                if i == 0:
                    print(distracting, tired, confidence, irritating)
# Calculate average SUS scores for each mode
average_sus_scores = {}
for mode, scores in sus_scores.items():
    if (mode in modes):
        average_score = sum(scores) / len(scores) if len(scores) > 0 else 0
    else:
        average_score = sum(scores)
    average_sus_scores[mode] = average_score

# Print and write to CSV
output_csv_filename = "sus_scores1.csv"
feedback_csv_filename = "feedback.csv"
with open(output_csv_filename, 'w', newline='') as output_csv_file:
    csv_writer = csv.writer(output_csv_file)
    csv_writer.writerow(["Mode", "Average SUS Score"])  # Write header
    for mode, score in average_sus_scores.items():
        csv_writer.writerow([mode, score])

with open(feedback_csv_filename, 'w', newline='') as feedback_csv_file:
    csv_writer = csv.writer(feedback_csv_file)
    csv_writer.writerow(["Mode", "Feedback"])  # Write header
    for mode, feedbacks in feedback.items():
        csv_writer.writerow([mode, feedbacks])
