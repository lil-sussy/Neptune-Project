// Canvas.tsx
import React, { useState, useRef, useEffect } from "react";
import { useDrop } from "react-dnd";
import { motion } from "framer-motion";
import Card from "./Card";
import styles from "./CardGrid.module.scss";

export interface Card {
	id: number;
	title: string;
	content: string;
}

export interface GridState {
	grid: (number | null)[];
	cards: Card[];
}

const Canvas = () => {
	const initialCards: Card[] = [
		{ id: 1, title: "Card 1", content: "This is the content of card 1" },
		{ id: 2, title: "Card 2", content: "This is the content of card 2" },
	];

	const initialGrid: (number | null)[] = Array(6).fill(null);
	initialGrid[0] = 1;
	initialGrid[1] = 2;

	const [cards, setCards] = useState<Card[]>(initialCards);
	const [grid, setGrid] = useState<(number | null)[]>(initialGrid);

  const canvasRef = useRef<HTMLDivElement>(null);

	const [{ isOver }, drop] = useDrop(() => ({
		accept: "CARD",
		drop: (item: Card, monitor) => {
      const cardID = Number(item.id);
			const delta = monitor.getClientOffset();
			if (delta && canvasRef.current) {
        const canvasRect = canvasRef.current.getBoundingClientRect();
				const x = Math.round((delta.x - canvasRect.left) / 260) -1;
				const y = Math.round((delta.y - canvasRect.top) / 230) -1;
				const index = y * 3 + x;
				console.log(`Dropping card ${cardID} at x: ${x}, y: ${y}, index: ${index}`);

				if (index >= 0 && index < grid.length) {
					setGrid((prev) => {
						const newGrid = [...prev];
						const oldIndex = newGrid.findIndex((id) => id === cardID);
						if (oldIndex !== -1) {
							newGrid[oldIndex] = null;
						}
						newGrid[index] = cardID;
						console.log(`Updated grid: ${JSON.stringify(newGrid)}`);
						return newGrid;
					});
				} else {
					console.error(`Calculated index ${index} is out of bounds`);
				}
			}
		},
		collect: (monitor) => ({
			isOver: monitor.isOver(),
		}),
	}));

  useEffect(() => {
		if (canvasRef.current) {
			drop(canvasRef.current);
		}
	}, [drop]);

	return (
		<div className={styles.canvas} ref={canvasRef}>
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
