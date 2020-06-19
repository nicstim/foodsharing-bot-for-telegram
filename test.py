# Рассылка по e-mail
import smtplib
smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
smtpObj.starttls()
smtpObj.login('lifeincodee@gmail.com','nenfnbcegth')
smtpObj.sendmail("justkiddingboat@gmail.com","sashapskov60@gmail.com","go to bed!")
smtpObj.quit()
