import re

data = "‎[3/11/2023, 11:00:25 am] Ukasha fateh jangi jahaz: ‎audio omitted\n" \
       "[3/11/2023, 9:18:49 pm] Haseeb jahaz library: @923456384840 bat sun\n" \
       "[3/11/2023, 9:19:02 pm] Haseeb jahaz library: Isky abu sy milwata hu tumy\n" \
       "‎[3/11/2023, 9:19:18 pm] Haseeb jahaz library: ‎image omitted\n" \
       "[3/11/2023, 9:19:45 pm] Ma'am Fahad: 😂😂😂\n" \
       "[3/11/2023, 9:41:33 pm] Ukasha fateh jangi jahaz: Alll the way from Londoooooon\n" \
       "[4/11/2023, 8:56:01 am] Umar Khayam: 🤣🤣🤣"

pattern = r"\[(.*?)\] (.*)"

# Using re.findall to find all occurrences in the multiline string
messages = re.findall(pattern, data)

for date_time, message in messages:
    # Split the sender from the message if needed
    sender_message_split = message.split(": ", 1)
    if len(sender_message_split) > 1:
        sender, text = sender_message_split
    else:
        sender = None  # No sender found before the message text
        text = sender_message_split[0]

    print(f"Date-Time: {date_time}")
    if sender:
        print(f"Sender: {sender}")
    print(f"Message: {text}\n")
