import React, { useState } from 'react';
import { ChevronUp, ChevronDown, Bell, HelpCircle, User } from 'lucide-react';
import BankBuddyLogo from './BankBuddyLogo';

const NestedFinancialCard = ({ title, subtitle, amount, children }) => {
  const [isExpanded, setIsExpanded] = useState(false);
  
  return (
    <div className="bg-slate-50 rounded-lg my-3">
      <div 
        className="flex justify-between items-center p-3 cursor-pointer hover:bg-slate-100 rounded-lg transition-colors"
        onClick={() => setIsExpanded(!isExpanded)}
      >
        <div>
          <div className="text-slate-800">{title}</div>
          <div className="text-sm text-slate-500">{subtitle}</div>
        </div>
        <div className="flex items-center space-x-4">
          {amount && <div className="text-slate-800 font-medium">{amount}</div>}
          {isExpanded ? <ChevronUp size={16} className="text-blue-900" /> : <ChevronDown size={16} className="text-blue-900" />}
        </div>
      </div>
      {isExpanded && (
        <div className="p-3 space-y-3 border-t border-slate-200">
          {children}
        </div>
      )}
    </div>
  );
};

const FinancialCard = ({ title, subtitle, children, defaultExpanded = true, actionButton }) => {
  const [isExpanded, setIsExpanded] = useState(defaultExpanded);
  
  return (
    <div className="bg-white rounded-lg shadow-sm mb-4 border border-blue-900">
      <div 
        className={`flex justify-between items-center p-4 ${children ? 'cursor-pointer rounded-lg hover:bg-slate-50 transition-colors' : ''}`}
        onClick={() => children && setIsExpanded(!isExpanded)}
      >
        <div>
          <h2 className="text-lg font-semibold text-blue-900">{title}</h2>
          <p className="text-sm text-slate-500">{subtitle}</p>
        </div>
        {actionButton ? (
          <div className="text-blue-900 text-sm hover:underline cursor-pointer" onClick={(e) => {
            e.stopPropagation();
            actionButton.onClick();
          }}>
            {actionButton.text}
          </div>
        ) : children && (
          isExpanded ? <ChevronUp size={20} className="text-blue-900" /> : <ChevronDown size={20} className="text-blue-900" />
        )}
      </div>
      {isExpanded && children && (
        <div className="border-t border-slate-100">
          <div className="p-4">
            {children}
          </div>
        </div>
      )}
    </div>
  );
};

const AccountItem = ({ title, subtitle, amount, subAmount }) => (
    <div className="py-2 px-3 -mx-3 cursor-pointer rounded-lg transition-colors group">
      <div className="flex justify-between items-start mb-1">
        <div className="text-slate-800 group-hover:text-blue-800 transition-colors">{title}</div>
        {amount && <div className="text-slate-700 font-medium group-hover:text-blue-800 transition-colors">{amount}</div>}
      </div>
      <div className="flex justify-between items-start">
        <div className="text-sm text-slate-500 group-hover:text-blue-700 transition-colors">{subtitle}</div>
        {subAmount && <div className="text-sm text-slate-500 group-hover:text-blue-700 transition-colors">{subAmount}</div>}
      </div>
    </div>
  );

const DashboardLayout = ({ children }) => {
  return (
    <div className="h-screen flex flex-col bg-slate-50">
      {/* Header */}
      <header className="bg-blue-900 border-b border-blue-800 flex-none text-white">
        <div className="max-w-7xl mx-auto px-4">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-8">
              <BankBuddyLogo />
              <nav className="space-x-6">
                <a href="#" className="text-white border-b-2 border-white pb-4">Home</a>
                <a href="#" className="text-blue-100 hover:text-white transition-colors">Banking</a>
                <a href="#" className="text-blue-100 hover:text-white transition-colors">Credit Card</a>
                <a href="#" className="text-blue-100 hover:text-white transition-colors">Invest</a>
              </nav>
            </div>
            <div className="flex items-center space-x-4">
              <button className="p-2 hover:bg-blue-800 rounded-full transition-colors">
                <HelpCircle size={20} className="text-white" />
              </button>
              <button className="p-2 hover:bg-blue-800 rounded-full transition-colors">
                <Bell size={20} className="text-white" />
              </button>
              <button className="flex items-center space-x-2 bg-slate-100 hover:bg-blue-100 text-blue-900 px-3 py-1 rounded transition-colors">
                <User size={16} />
                <span>Jane</span>
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="flex-1 overflow-hidden">
        <div className="max-w-7xl mx-auto px-4 h-full">
          <h2 className="text-3xl font-semibold text-slate-900 py-6">Hi, Jane!</h2>
          
          <div className="flex gap-6 h-[calc(100vh-11rem)]">
            {/* Left Column - Financial Information */}
            <div className="w-1/2 overflow-y-auto pr-3">
              <FinancialCard 
                title="Banking" 
                subtitle="5 transactions today"
              >
                <NestedFinancialCard
                  title="Bank of America"
                  subtitle="Total Amount"
                  amount="$20,003.78"
                >
                  <AccountItem 
                    title="Checking Account" 
                    amount="$3,000.00"
                  />
                  <AccountItem 
                    title="Savings Account" 
                    amount="$17,000.78"
                  />
                </NestedFinancialCard>

                <NestedFinancialCard
                  title="JP Morgan Chase"
                  subtitle="Total Amount"
                  amount="$40,039.00"
                >
                  <AccountItem 
                    title="Checking Account" 
                    amount="$40,039.00"
                  />
                </NestedFinancialCard>

                <NestedFinancialCard
                  title="American Express"
                  subtitle="Total Amount"
                  amount="$305,029.00"
                >
                  <AccountItem 
                    title="Checking Account" 
                    amount="$155,000.00"
                  />
                  <AccountItem 
                    title="Savings Account" 
                    amount="$150,029.00"
                  />
                </NestedFinancialCard>
              </FinancialCard>

              <FinancialCard 
                title="Credit Card" 
                subtitle="Available credit"
              >
                <NestedFinancialCard
                  title="Bank of America Customized Cash Rewards"
                  subtitle="Available credit"
                  amount="$8,500.00"
                >
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
                </NestedFinancialCard>

                <NestedFinancialCard
                  title="Chase Sapphire Reserve"
                  subtitle="Available credit"
                  amount="$12,000.00"
                >
                  <AccountItem 
                    title="Current Balance" 
                    subtitle="Statement closes in 8 days"
                    amount="$2,750.45"
                  />
                  <AccountItem 
                    title="Pending Charges" 
                    subtitle="1 transaction"
                    amount="$125.00"
                  />
                </NestedFinancialCard>

                <NestedFinancialCard
                  title="American Express Gold"
                  subtitle="Available credit"
                  amount="$15,000.00"
                >
                  <AccountItem 
                    title="Current Balance" 
                    subtitle="Statement closes in 21 days"
                    amount="$3,245.67"
                  />
                  <AccountItem 
                    title="Pending Charges" 
                    subtitle="3 transactions"
                    amount="$478.92"
                  />
                </NestedFinancialCard>
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
                title="Relay Insights" 
                subtitle="4 Bank of America accounts"
              >
                <AccountItem 
                  title="Cash" 
                  subtitle="1 Bank of America account | 2 SoFi accounts"
                  amount="$14,802.45"
                />
                <div className="border-t border-gray-100 my-3" />
                <AccountItem 
                  title="Investments" 
                  subtitle="2 Fidelity accounts"
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
                title="Loans" 
                subtitle="Find a loan for you"
                actionButton={{
                  text: "Check your rate",
                  onClick: () => console.log("Check rate clicked")
                }}
              />

            </div>

            {/* Right Column - Chat Interface */}
            <div className="w-1/2 flex flex-col rounded-3xl bg-white">
              {children}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
export default DashboardLayout;