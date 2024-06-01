import React from "react";
import { useDrag } from "react-dnd";
import { motion } from "framer-motion";
import styles from "./Card.module.scss";

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
				scale: 1.1,
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
				<div className={styles.ellipse1}></div>
				<div className={styles.newFileEmptyCommonFileContent}>
					<div className={styles.newFileEmptyCommonFileContentInner}>
						<div className={styles.vector}></div>
						<div className={styles.vector2529}></div>
					</div>
				</div>
			</div>
			<div className={styles.mainContent}>
				<div className={styles.container}>
					<div className={styles.cardTitle}>{title}</div>
					<div className={styles.cardContent}>{content}</div>
				</div>
				<div className={styles.actions}>
					<div className={styles.editButton}>
						<div className={styles.vector}></div>
						<div className={styles.rectangle17}></div>
					</div>
					<div className={styles.readEverything}>Read everything</div>
				</div>
			</div>
			<div className={styles.scrollbar}></div>
		</motion.div>
	);
};

export default Card;
