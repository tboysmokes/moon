"""

print(''' SELECT users.firstname, users.lastname, users.email, users.phonenumber, users.passwords, 
          account.account_name, account.account_num,
          secaccount.account_name, secaccount.account_num,
          thirdaccount.account_name, thirdaccount.account_num
          FROM users 
          LEFT JOIN account ON users.ID = account.userID 
          LEFT JOIN secaccount ON account.userID = secaccount.userID
          LEFT JOIN thirdaccount ON secaccount.userID = thirdaccount.userID
          WHERE users.ID = ?''', (userid))

firstname   
lastname       
email            
phonenumber     
password

account
account_name
account_num

secaccount
account_name
account_num

thirdaccount
account_name
account_num

"""