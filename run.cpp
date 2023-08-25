#include <iostream>
#include <fstream>
#include <string>

using namespace std;

// withdrawl
// check balane
// tranfer
string cardnumber;

class machine
{
private:
	int pin;
	double ammount;
	double atmCash = 100000;
	// you are to add a total amount which the atm carries

public:
	void login();
	void withdrawals();
	void deposit();
	void tranfer();
	void getbalance();
	void changePass();
	void forgotpass();
};

int main()
{
up:
	string comcard;
	char c;
	int pin;
	int compin;
	machine call;

	cout << "enter your card number : ";
	cin >> cardnumber;
	cout << "enter your pin : ";
	cin >> pin;

	for (size_t i = 0; i < cardnumber.length(); i++)
	{
		c = cardnumber[i];
	}

	if (cardnumber.length() != 10)
	{
		cout << "the card numbr you enter is either less than or greater 10 " << endl;
		cout << "please try again " << endl;
		goto up;
	}
	else
	{
		ifstream file;
		file.open(cardnumber + ".txt");

		if (file.is_open())
		{
			cout << "account found" << endl;

			while (file >> comcard >> compin)
			{
				if (cardnumber == comcard && pin == compin)
				{
					call.login();
				}
				else
				{
					cout << "incorrect pin or card number ";
					goto up;
				}
			}
		}
		else
		{
			cout << "error occured try again later";
			exit(0);
		}
	}
}

void machine::login()
{
	int answer;

	cout << "\t\t\t\t|_____________WELCOME TO PRO BANK_______________|" << endl;
	cout << "\t\t\t\t|                                               |" << endl;
	cout << "\t\t\t\t|          press 1) To withdrawal               |" << endl;
	cout << "\t\t\t\t|          press 2) To deposit                  |" << endl;
	cout << "\t\t\t\t|          press 3) To tranfer                  |" << endl;
	cout << "\t\t\t\t|          press 4) To check balance            |" << endl;
	cout << "\t\t\t\t|          press 5) To change password          |" << endl;
	cout << "\t\t\t\t|          press 6) forgot password             |" << endl;
	cout << "\t\t\t\t|          press 7) To exit                     |" << endl;
	cout << "\t\t\t\t|_______________________________________________|" << endl;
	cin >> answer;

	switch (answer)
	{
	case 1:
	{
		withdrawals();
		break;
	}
	case 2:
	{
		deposit();
		break;
	}
	case 3:
	{
		tranfer();
		break;
	}
	case 4:
	{
		getbalance();
		break;
	}
	case 5:
	{
		changePass();
		break;
	}
	case 6:
	{
		forgotpass();
		break;
	}
	case 7:
	{
		exit(0);
		break;
	}
	}
}

void machine::withdrawals()
{
    if (atmCash > 0)
    {
        double amount2;

        cout << "how much would you like to withdraw: ";
        cin >> amount2;

        if (amount2 > atmCash) {
            cout << "ATM does not have enough cash." << endl;
            login();
            return;
        }

        ifstream file;
        file.open(cardnumber + ".txt");
        file >> cardnumber >> pin >> ammount;
        file.close();
   
		cout<<"account balance : "<<ammount<<endl;

        if (amount2 > ammount) {
            cout << "Insufficient balance." << endl;
            login();
            return;
        }

        ammount -= amount2;
        atmCash -= amount2;

        ofstream details;
        details.open(cardnumber + ".txt");
        details << cardnumber << endl
                << pin << endl
                << ammount;
        details.close();

        cout << "Withdrawal successful." << endl;
        login();
    }
    else
    {
        cout << "Sorry, ATM is out of cash." << endl;
        login();
    }
}


void machine::deposit()
{

	double amount2;

	cout << "how much would like to deposit : ";
	cin >> amount2;

	ifstream file;
	file.open(cardnumber + ".txt");

	file >> cardnumber >> pin >> ammount;

	ammount = ammount + amount2;
	file.close();

	ofstream details;
	details.open(cardnumber + ".txt");
	details << cardnumber << endl
			<< pin << endl
			<< ammount;

	details.close();

	cout << "deposit successful " << endl;
	login();
}

void machine::tranfer()
{
up:

	string cardid;
	string recivecardi;
	string sendercard;
	int recivepin;
	double amount;
	double reciveamount;

	cout << "Enter the number you would like to tranfer to : ";
	cin >> cardid;

	ifstream file;
	file.open(cardid + ".txt");
	file >> recivecardi >> recivepin >> reciveamount;

	ifstream data;
	data.open(cardnumber + ".txt");
	data >> sendercard >> pin >> ammount;

	if (file.is_open() && data.is_open())
	{
		cout<<"your balance is "<<ammount<<endl;
		cout << "how much would you like to tranfer: ";
		cin >> amount;

		if (amount > ammount)
		{
			cout << "insufficient funds" << endl;
			goto up;
		}
		data.close();
		file.close();

		ammount -= amount;
		reciveamount += amount;

		ofstream details;
		ofstream edit;

		edit.open(cardnumber + ".txt");
		details.open(cardid + ".txt");

		edit << sendercard << endl
			 << pin << endl
			 << ammount << endl;

		details << recivecardi << endl
				<< recivepin << endl
				<< reciveamount << endl;

		edit.close();
		details.close();

		cout << "tranfer successfull " << endl;
		login();
	}
}

void machine::getbalance()
{
	ifstream file;
	file.open(cardnumber + ".txt");
	file >> cardnumber >> pin >> ammount;
	cout << "you balanace is " << ammount << endl;

	login();
}

void machine::changePass()
{
up:

	string cardid;
	int pins;
	int oldpin;
	int newpin;
	int conpin;
	double amount;

	ifstream data;
	data.open(cardnumber + ".txt");
	data >> cardid >> pins >> amount;

	cout << "enter the old pin : ";
	cin >> oldpin;
	cout << "enter the new password : ";
	cin >> newpin;
	data.close();

	if (pins == oldpin)
	{
		ofstream file;
		file.open(cardnumber + ".txt");
		file << cardid << endl
			 << newpin << endl
			 << amount << endl;

		cout << "password change successful " << endl;
		login();
	}
	else
	{
		cout << "error changing password ";
		cout << "either the old password is incorrect" << endl;
		cout << "or the new one does not match " << endl;
		goto up;
	}
}

void machine::forgotpass()
{
up:

	int oldPin;
	string cardid;
	double amount;

	ifstream data;
	data.open(cardnumber + ".txt");
	data>>cardid>>oldPin>>amount;

	cout<<"your password is "<<oldPin<<endl;

	data.close();
	login();
}