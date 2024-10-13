import React, { ReactNode } from 'react';
import Link from 'next/link';

interface LayoutProps {
  children: ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <div className="min-h-screen flex flex-col">
      <nav className="bg-indigo-600">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center">
              <Link href="/" className="text-white font-bold text-xl">
                AIGENT
              </Link>
            </div>
            <div className="hidden md:block">
              <div className="ml-10 flex items-baseline space-x-4">
                <Link href="/data-file-creation" className="text-gray-300 hover:bg-indigo-700 hover:text-white px-3 py-2 rounded-md text-sm font-medium">
                  Data File Creation
                </Link>
                <Link href="/data-set-creation" className="text-gray-300 hover:bg-indigo-700 hover:text-white px-3 py-2 rounded-md text-sm font-medium">
                  Data Set Creation
                </Link>
                <Link href="/agent-training" className="text-gray-300 hover:bg-indigo-700 hover:text-white px-3 py-2 rounded-md text-sm font-medium">
                  Agent Training
                </Link>
                <Link href="/agent-creation" className="text-gray-300 hover:bg-indigo-700 hover:text-white px-3 py-2 rounded-md text-sm font-medium">
                  Agent Creation
                </Link>
              </div>
            </div>
          </div>
        </div>
      </nav>

      <main className="flex-grow bg-gray-100">
        <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
          {children}
        </div>
      </main>

      <footer className="bg-gray-800 text-white text-center py-4">
        <p>&copy; 2024 AIGENT. All rights reserved.</p>
      </footer>
    </div>
  );
};

export default Layout;
