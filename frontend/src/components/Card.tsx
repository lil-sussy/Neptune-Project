import React from "react";
import { useDrag } from "react-dnd";
import { motion } from "framer-motion";
import styles from "./Card.module.scss";
import { CardIcon, EditIcon } from "./Icon";

interface CardProps {
	id: string;
	title: string;
	content: string;
}

const Card: React.FC<CardProps> = ({ id, title, content }) => {
	const [{ isDragging }, drag] = useDrag(() => ({
		type: "CARD",
		item: { id },
		collect: (monitor) => ({
			isDragging: monitor.isDragging(),
		}),
	}));

	return (
		<motion.div
			className={styles.card}
			ref={drag}
			style={{ opacity: isDragging ? 0.5 : 1 }}
			whileHover={{
				boxShadow: "0px 5px 15px rgba(0, 0, 0, 0.2)",
				transition: { duration: 0.3 },
			}}
			whileDrag={{
				scale: 1.2,
				rotate: 5,
				boxShadow: "0px 10px 20px rgba(0, 0, 0, 0.3)",
				transition: { duration: 0.3 },
			}}
			animate={{
				boxShadow: isDragging ? "0px 10px 20px rgba(0, 0, 0, 0.3)" : "0px 5px 15px rgba(0, 0, 0, 0.1)",
			}}
			exit={{
				opacity: 0,
				transition: { duration: 0.5 },
			}}
		>
			<div className={styles.icon}>
        <CardIcon />
			</div>
			<div className={styles.mainContent}>
				<div className={styles.container}>
					<div className={styles.cardTitle}>{title}</div>
					<div className={styles.cardContent}>{content}</div>
				</div>
				<div className={styles.actions}>
					<div className={styles.editButton}>
            <EditIcon />
					</div>
					<div className={styles.readEverything}>Read everything</div>
				</div>
			</div>
		</motion.div>
	);
};

export default Card;
