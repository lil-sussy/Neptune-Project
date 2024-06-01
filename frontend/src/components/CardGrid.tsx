// Canvas.tsx
import React, { useState } from "react";
import { useDrop } from "react-dnd";
import { motion } from "framer-motion";
import Card from "./Card";
import styles from "./CardGrid.module.scss";

const gridPositions = [
	{ x: 0, y: 0 },
	{ x: 1, y: 0 },
	{ x: 2, y: 0 },
	{ x: 0, y: 1 },
	{ x: 1, y: 1 },
	{ x: 2, y: 1 },
];

const Canvas = () => {
	const [cards, setCards] = useState([
		{ id: 1, title: "Card 1", content: "This is the content of card 1" },
		{ id: 2, title: "Card 2", content: "This is the content of card 2" },
	]);
  const emptyGrid = Array(4).fill(null);
  emptyGrid.push(1);
  emptyGrid.push(2);
	const [grid, setGrid] = useState(emptyGrid);

	const [{ isOver }, drop] = useDrop(() => ({
		accept: "CARD",
		drop: (item: any, monitor) => {
			const delta = monitor.getClientOffset();
			if (delta) {
				const x = Math.round(delta.x / 200);
				const y = Math.round(delta.y / 150);
				const index = y * 3 + x;
				setGrid((prev) => {
					const newGrid = [...prev];
					newGrid[index] = item.id;
					return newGrid;
				});
			}
		},
		collect: (monitor) => ({
			isOver: monitor.isOver(),
		}),
	}));

	return (
		<div className={styles.canvas} ref={drop}>
			{grid.map((cardId, index) => {
				const card = cards.find((card) => card.id === cardId);
				return (
					<motion.div key={index} className={styles.gridItem} whileHover={{ scale: 1.05 }} animate={{ backgroundColor: isOver ? "#eee" : "#fff" }}>
						{card ? <Card id={card.id.toString()} title={card.title} content={card.content} /> : null}
					</motion.div>
				);
			})}
		</div>
	);
};

export default Canvas;
