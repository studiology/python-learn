hrs = raw_input("Enter Hours:")
h = float(hrs)
rate = raw_input("Enter Hourly Rate:")
r = float(rate)

if h<=40 :
    pay = h * r
else:
    pay = (40 * r) + ((h - 40) * r * 1.5)

print pay
