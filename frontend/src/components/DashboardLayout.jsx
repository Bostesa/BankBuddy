import React, { useState } from 'react';
import { ChevronUp, ChevronDown, Bell, HelpCircle, User } from 'lucide-react';

const FinancialCard = ({ title, subtitle, children, defaultExpanded = true, actionButton }) => {
  const [isExpanded, setIsExpanded] = useState(defaultExpanded);
  
  return (
    <div className="bg-white rounded-lg shadow-sm mb-4 border border-gray-200">
      <div 
        className={`flex justify-between items-center p-4 ${children ? 'cursor-pointer' : ''}`}
        onClick={() => children && setIsExpanded(!isExpanded)}
      >
        <div>
          <h2 className="text-lg font-semibold text-gray-800">{title}</h2>
          <p className="text-sm text-gray-500">{subtitle}</p>
        </div>
        {actionButton ? (
          <div className="text-blue-500 text-sm hover:underline cursor-pointer" onClick={(e) => {
            e.stopPropagation();
            actionButton.onClick();
          }}>
            {actionButton.text}
          </div>
        ) : children && (
          isExpanded ? <ChevronUp size={20} /> : <ChevronDown size={20} />
        )}
      </div>
      {isExpanded && children && (
        <div className="border-t border-gray-100">
          <div className="p-4 space-y-3">
            {children}
          </div>
        </div>
      )}
    </div>
  );
};

const AccountItem = ({ title, subtitle, amount, subAmount }) => (
  <div className="py-2">
    <div className="flex justify-between items-start mb-1">
      <div className="text-gray-800">{title}</div>
      {amount && <div className="text-gray-800 font-medium">{amount}</div>}
    </div>
    <div className="flex justify-between items-start">
      <div className="text-sm text-gray-500">{subtitle}</div>
      {subAmount && <div className="text-sm text-gray-500">{subAmount}</div>}
    </div>
  </div>
);

const DashboardLayout = ({ children }) => {
  return (
    <div className="h-screen flex flex-col bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 flex-none">
        <div className="max-w-7xl mx-auto px-4">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-8">
              <div className="text-2xl font-bold text-blue-500">SoFi</div>
              <nav className="space-x-6">
                <a href="#" className="text-blue-500 border-b-2 border-blue-500 pb-4">Home</a>
                <a href="#" className="text-gray-500">Banking</a>
                <a href="#" className="text-gray-500">Credit Card</a>
                <a href="#" className="text-gray-500">Invest</a>
              </nav>
            </div>
            <div className="flex items-center space-x-4">
              <button className="p-2">
                <HelpCircle size={20} />
              </button>
              <button className="p-2">
                <Bell size={20} />
              </button>
              <button className="flex items-center space-x-2 bg-blue-500 text-white px-3 py-1 rounded">
                <User size={16} />
                <span>Nathan</span>
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="flex-1 overflow-hidden">
        <div className="max-w-7xl mx-auto px-4 h-full">
          <h1 className="text-3xl font-semibold text-gray-800 py-6">Hi Nathan</h1>
          
          <div className="flex gap-6 h-[calc(100vh-11rem)]">
            {/* Left Column - Financial Information */}
            <div className="w-1/2 overflow-y-auto pr-3">
              <FinancialCard 
                title="Banking" 
                subtitle="0 transactions today"
              >
                <AccountItem 
                  title="Checking" 
                  subtitle="0 transactions today"
                  amount="$5,021.00"
                />
                <div className="border-t border-gray-100 my-3" />
                <AccountItem 
                  title="Savings" 
                  subtitle="Saved this month"
                  amount="$25,200.59"
                />
              </FinancialCard>

              <FinancialCard 
                title="Credit Card" 
                subtitle="Available credit"
              >
                <AccountItem 
                  title="SoFi Credit Card" 
                  subtitle="Available credit"
                  amount="$8,500.00"
                />
                <AccountItem 
                  title="Current Balance" 
                  subtitle="Statement closes in 15 days"
                  amount="$1,500.00"
                />
                <AccountItem 
                  title="Pending Charges" 
                  subtitle="2 transactions"
                  amount="$245.33"
                />
              </FinancialCard>

              <FinancialCard 
                title="Invest" 
                subtitle="5 accounts"
              >
                <AccountItem 
                  title="Active Invest" 
                  subtitle="3 positions"
                  amount="$15,750.82"
                />
                <div className="border-t border-gray-100 my-3" />
                <AccountItem 
                  title="Automated Investing" 
                  subtitle="Moderate strategy"
                  amount="$8,245.65"
                />
                <div className="border-t border-gray-100 my-3" />
                <AccountItem 
                  title="Cryptocurrency" 
                  subtitle="4 assets"
                  amount="$2,571.42"
                />
              </FinancialCard>

              <FinancialCard 
                title="Relay Insights" 
                subtitle="4 SoFi accounts"
              >
                <AccountItem 
                  title="Cash" 
                  subtitle="2 SoFi accounts"
                  amount="$14,802.45"
                />
                <div className="border-t border-gray-100 my-3" />
                <AccountItem 
                  title="Investments" 
                  subtitle="2 SoFi accounts"
                  amount="$28,567.89"
                />
                <div className="border-t border-gray-100 my-3" />
                <AccountItem 
                  title="Credit cards" 
                  subtitle="0 accounts"
                  amount="$0.00"
                />
                <div className="text-blue-500 text-sm mt-4 cursor-pointer hover:underline">
                  View all (4)
                </div>
              </FinancialCard>

              <FinancialCard 
                title="Relay Connections" 
                subtitle="7 SoFi | 18 external accounts"
              >
                <AccountItem 
                  title="Connected Accounts" 
                  subtitle="Total value across accounts"
                  amount="$157,890.45"
                />
                <div className="border-t border-gray-100 my-3" />
                <AccountItem 
                  title="External Accounts" 
                  subtitle="18 accounts"
                  amount="$89,275.23"
                />
              </FinancialCard>

              <FinancialCard 
                title="Credit Score" 
                subtitle="Updated on 2/6"
              >
                <AccountItem 
                  title="FICO® Score" 
                  subtitle="Excellent"
                  amount="785"
                />
                <div className="border-t border-gray-100 my-3" />
                <AccountItem 
                  title="Score Change" 
                  subtitle="Since last month"
                  amount="+12"
                />
              </FinancialCard>

              <FinancialCard 
                title="Loans" 
                subtitle="Find a loan for you"
                actionButton={{
                  text: "Check your rate",
                  onClick: () => console.log("Check rate clicked")
                }}
              />
            </div>

            {/* Right Column - Chat Interface */}
            <div className="w-1/2 flex flex-col">
              {children}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DashboardLayout;