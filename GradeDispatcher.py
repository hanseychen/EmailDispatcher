import csv
import os
from string import Template


# Load email title, email content for full score students, and email content for
# students who made mistakes, from corresponding files.
def load_templates():
    with open('email-subject.txt', 'r') as subject_file:
        subject = subject_file.read()
    with open('email-content-smooth.txt', 'r') as smooth_file:
        content_smooth = smooth_file.read()
    with open('email-content-bumped.txt', 'r') as bumped_file:
        content_bumped = bumped_file.read()
    return subject.strip(), content_smooth.strip(), content_bumped.strip()


# Load students' email addresses, corresponding scores, and reasons for lost
# points, from corresponding files.
def load_scores():
    with open('email-addresses.txt', 'rb') as address_file:
        addresses = []
        for line in address_file:
            addresses.append(line.strip())
    with open('scores.csv', 'rb') as csv_file:
        csv_content = csv.reader(csv_file)
        scores = []
        reasons = []
        for row in csv_content:
            scores.append(row[0])
            reasons.append(row[1])
    return addresses, scores, reasons


# Fill the email template with student's score and the reasons he loses score.
def fill_template(template_file, score, reasons):
    template = Template(template_file)
    template = template.substitute(SCORE=str(score), REASONS=str(reasons))
    return template


# Generate the corresponding AppleScript to send the email.
def generate_script(subject, content, address):
    with open('script-template.txt', 'rb') as source_template:
        script_source = Template(source_template.read())
        script_source = script_source.substitute(SUBJECT=str(subject),
                                                 CONTENT=str(content),
                                                 ADDRESS=str(address))
        with open('real-script.txt', 'w') as real_source:
            real_source.write(script_source)


# Compile and run the AppleScript
def compile_and_run():
    os.system('touch SendEmail.scpt')
    os.system('osacompile -o SendEmail.scpt real-script.txt')
    os.system('osascript SendEmail.scpt')
    os.system('rm SendEmail.scpt')


def main():
    subject, content_smooth, content_bumped = load_templates()

    addresses, scores, reasons = load_scores()

    for i in range(0, len(addresses)):
        if scores[i] == '100':
            content = content_smooth
        else:
            content = fill_template(content_bumped, scores[i], reasons[i])

        generate_script(subject, content, addresses[i])
        compile_and_run()


if __name__ == '__main__':
    main()
