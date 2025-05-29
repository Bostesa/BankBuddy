// DashboardLayout.jsx
import React, { useState } from 'react';
import { ChevronUp, ChevronDown, Bell, HelpCircle, User } from 'lucide-react';
import BankBuddyLogo from './BankBuddyLogo';
import { useAccounts } from '../hooks/useAccounts';

//
// Minimal FinancialCard component
//
const FinancialCard = ({ title, subtitle, children, defaultExpanded = true }) => {
  const [isExpanded, setIsExpanded] = useState(defaultExpanded);

  return (
    <div className="bg-white rounded-lg shadow-sm mb-4 p-4 border border-blue-900 w-full">
      <div
        className="flex justify-between items-center cursor-pointer"
        onClick={() => setIsExpanded(!isExpanded)}
      >
        <div>
          <h2 className="text-lg font-semibold text-blue-900">{title}</h2>
          <p className="text-sm text-slate-500">{subtitle}</p>
        </div>
        {isExpanded ? (
          <ChevronUp size={20} className="text-blue-900" />
        ) : (
          <ChevronDown size={20} className="text-blue-900" />
        )}
      </div>
      {isExpanded && (
        <div className="mt-4 space-y-3">
          {children}
        </div>
      )}
    </div>
  );
};

//
// Updated AccountItem to display balance and optional purchaseBalance
//
const AccountItem = ({ title, balance, purchaseBalance }) => (
  <div className="py-2 border-b border-slate-100">
    <div className="text-blue-900 font-medium">{title}</div>
    <div className="text-sm text-slate-500">{`Balance: $${balance.toFixed(2)}`}</div>
    {purchaseBalance !== undefined && (
      <div className="text-sm text-slate-500">{`Purchase Balance: $${purchaseBalance.toFixed(2)}`}</div>
    )}
  </div>
);

//
// The main DashboardLayout
//
const DashboardLayout = ({ children }) => {
  // Use the custom hook to fetch accounts from /accounts/
  const { accounts, loading, error } = useAccounts();

  // Separate account types
  const bankingAccounts = accounts.filter(a => a.account_type === 'checking' || a.account_type === 'savings');
  const creditCardAccounts = accounts.filter(a => a.account_type === 'credit_card');
  const brokerageAccounts = accounts.filter(a => a.account_type === 'brokerage');

  return (
    <div className="h-screen flex flex-col bg-slate-50">
      {/* Header */}
      <header className="bg-blue-900 border-b border-blue-800 text-white flex-none">
        <div className="flex items-center justify-between px-4 h-16 w-full">
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
              <span>Nathan</span>
            </button>
          </div>
        </div>
      </header>

      {/* Main Content Area */}
      <div className="flex-1 flex overflow-hidden">
        {/* Left Column - Financial Info */}
        <div className="w-1/2 overflow-y-auto p-4 flex flex-col">
          {loading && <p className="text-slate-700">Loading accounts...</p>}
          {error && <p className="text-red-600">Error: {error}</p>}

          {!loading && !error && (
            <>
              {/* Banking (Checking + Savings) */}
              <FinancialCard title="Banking" subtitle="Checking & Savings">
                {bankingAccounts.map(acc => (
                  <AccountItem
                    key={acc.id}
                    title={acc.account_name}
                    balance={acc.balance}
                  />
                ))}
              </FinancialCard>

              {/* Credit Card Accounts */}
              <FinancialCard title="Credit Cards" subtitle="All credit accounts">
                {creditCardAccounts.map(acc => (
                  <AccountItem
                    key={acc.id}
                    title={acc.account_name}
                    balance={acc.balance}
                  />
                ))}
              </FinancialCard>

              {/* Brokerage Accounts with purchase_balance */}
              <FinancialCard title="Invest" subtitle="Brokerage Accounts">
                {brokerageAccounts.map(acc => (
                  <AccountItem
                    key={acc.id}
                    title={acc.account_name}
                    balance={acc.balance}
                    purchaseBalance={acc.purchase_balance}
                  />
                ))}
              </FinancialCard>
            </>
          )}
        </div>

        {/* Right Column - Chat or Other Children */}
        <div className="w-1/2 bg-white p-4 flex flex-col">
          {children}
        </div>
      </div>
    </div>
  );
};

export default DashboardLayout;
