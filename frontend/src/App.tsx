import React from 'react';
import logo from './logo.svg';
import './App.css';
import MainApp from './components/MainApp';
import "antd/dist/reset.css"
import { Button, ConfigProvider, Input, Space, theme } from "antd";

function App() {
  return (
		<ConfigProvider
			theme={{
				// 1. Use dark algorithm
				algorithm: theme.darkAlgorithm,

				// 2. Combine dark algorithm and compact algorithm
				// algorithm: [theme.darkAlgorithm, theme.compactAlgorithm],
			}}
		>
      <div className="App">
        <header className="App-header">
          <MainApp />
        </header>
      </div>
		</ConfigProvider>
	);
}

export default App;
