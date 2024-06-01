import React, { useState } from "react";
import styles from "./MainApp.module.scss";
import { MailOutlined } from "@ant-design/icons";
import type { MenuProps, MenuTheme } from "antd";
import { Menu, Switch } from "antd";
import { Input } from "antd";
import { Button } from "antd";
import CardGrid from "./CardGrid";
import { DndProvider } from "react-dnd";
import { HTML5Backend } from "react-dnd-html5-backend";

const { TextArea } = Input;
const { Search } = Input;

type MenuItem = Required<MenuProps>["items"][number];

function App() {
	const [inputValue, setInputValue] = useState("");
  const [current, setCurrent] = useState("1");

  const items: MenuItem[] = [
		{
			key: "sub1",
			icon: <MailOutlined />,
			label: "Navigation One",
		},
		{ key: "5", label: "Option 5" },
		{ key: "6", label: "Option 6" },
	];

	const onClick: MenuProps["onClick"] = (e) => {
		setCurrent(e.key);
	};

  
	return (
		<div className={styles.appContainer}>
			<div className={styles.topBar}>
				<div className={styles.topBarLeft}>
					<h1>Neptune Project</h1>
				</div>
				<div className={styles.topBarRight}>
					<Button type="text">Secondary</Button>
					<Button type="primary">Primary</Button>
				</div>
			</div>
			<div className={styles.mainContainer}>
        <div className={styles.textInputContainer}>
          <TextArea rows={4}  id="main-input" placeholder="Type something" value={inputValue} onChange={(e) => setInputValue(e.target.value)} className={styles.textInput} />
        </div>
				<div className={styles.leftSidebar}>
					<h5>37 elements</h5>
					<Menu onClick={onClick} style={{ width: 256 }} openKeys={["sub1"]} selectedKeys={[current]} mode="vertical" theme="dark" items={items} getPopupContainer={(node) => node.parentNode as HTMLElement} />
					<div className={styles.historyContainer}>
						<div className={styles.historyElement}></div>
					</div>
				</div>
				<div className={styles.mainContent}>
          <DndProvider backend={HTML5Backend}>
            <CardGrid />
          </DndProvider>
				</div>
				<div className={styles.rightSidebar}>
					<Search id="search-bar" placeholder="Search" className={styles.searchBar} />
				</div>
			</div>
		</div>
	);
}

export default App;
