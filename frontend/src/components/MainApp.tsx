import React, { useState } from "react";
import { TextInput, Button, Search, Grid, Row, Column, TextArea } from "@carbon/react";
import styles from "./MainApp.module.scss";

function App() {
	const [inputValue, setInputValue] = useState("");

	return (
		<div className={styles.appContainer}>
			<div className={styles.mainContent}>
				<div className={styles.mainContent}>
					<div className={styles.topContainer}>
						<p>Top container content</p>
					</div>
					<div className={styles.bottomContainer}>
						<p>Bottom container content</p>
					</div>
				</div>
				<div className={styles.textInputContainer}>
					<TextArea id="main-input" labelText="Type something" value={inputValue} onChange={(e) => setInputValue(e.target.value)} className={styles.textInput} />
				</div>
			</div>
			<div className={styles.rightSidebar}>
				<Search id="search-bar" labelText="Search" className={styles.searchBar} />
				<div className={styles.topContainer}>
					<p>Top container content</p>
				</div>
				<div className={styles.bottomContainer}>
					<p>Bottom container content</p>
				</div>
			</div>
		</div>
	);
}

export default App;
