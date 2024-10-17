-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Oct 17, 2024 at 04:22 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `trading`
--

-- --------------------------------------------------------

--
-- Table structure for table `alembic_version`
--

CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `alembic_version`
--

INSERT INTO `alembic_version` (`version_num`) VALUES
('8be3026b664f');

-- --------------------------------------------------------

--
-- Table structure for table `cash_transactions`
--

CREATE TABLE `cash_transactions` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `transaction_type` varchar(10) NOT NULL,
  `amount` float NOT NULL,
  `timestamp` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `cash_transactions`
--

INSERT INTO `cash_transactions` (`id`, `user_id`, `transaction_type`, `amount`, `timestamp`) VALUES
(1, 1, 'deposit', 1000, '2024-10-15 10:00:00'),
(2, 2, 'withdrawal', 500, '2024-10-15 11:00:00'),
(3, 3, 'deposit', 2000, '2024-10-15 12:00:00'),
(4, 4, 'withdrawal', 300, '2024-10-15 13:00:00'),
(5, 5, 'deposit', 1500, '2024-10-15 14:00:00');

-- --------------------------------------------------------

--
-- Table structure for table `market_hours`
--

CREATE TABLE `market_hours` (
  `id` int(11) NOT NULL,
  `start_time` time NOT NULL,
  `end_time` time NOT NULL,
  `weekdays_only` tinyint(1) DEFAULT NULL,
  `holiday_closure` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `stock_id` int(11) NOT NULL,
  `order_type` varchar(4) NOT NULL,
  `quantity` int(11) NOT NULL,
  `price` float NOT NULL,
  `status` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` (`id`, `user_id`, `stock_id`, `order_type`, `quantity`, `price`, `status`) VALUES
(1, 1, 1, 'buy', 50, 150, 'executed'),
(2, 5, 1, 'buy', 101, 2800.02, 'pending'),
(3, 3, 3, 'sell', 5, 3400, 'cancelled'),
(4, 4, 4, 'buy', 20, 900, 'executed'),
(5, 5, 5, 'sell', 100, 290, 'pending'),
(7, 2, 1, 'sell', 12, 4343.98, 'pending'),
(8, 5555, 2, 'buy', 12, 32434.8, 'pending');

-- --------------------------------------------------------

--
-- Table structure for table `portfolios`
--

CREATE TABLE `portfolios` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `cash_balance` float DEFAULT NULL,
  `total_value` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `portfolios`
--

INSERT INTO `portfolios` (`id`, `user_id`, `cash_balance`, `total_value`) VALUES
(1, 1, 10000, 15000),
(2, 2, 5000, 7000),
(3, 3, 20000, 25000),
(4, 4, 3000, 6000),
(5, 5, 15000, 20000);

-- --------------------------------------------------------

--
-- Table structure for table `portfolio_stocks`
--

CREATE TABLE `portfolio_stocks` (
  `id` int(11) NOT NULL,
  `portfolio_id` int(11) NOT NULL,
  `stock_id` int(11) NOT NULL,
  `quantity` int(11) NOT NULL,
  `average_price` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `portfolio_stocks`
--

INSERT INTO `portfolio_stocks` (`id`, `portfolio_id`, `stock_id`, `quantity`, `average_price`) VALUES
(1, 1, 1, 50, 150),
(2, 2, 2, 10, 2800),
(3, 3, 3, 5, 3400),
(4, 4, 4, 20, 900),
(5, 5, 5, 100, 290);

-- --------------------------------------------------------

--
-- Table structure for table `stocks`
--

CREATE TABLE `stocks` (
  `id` int(11) NOT NULL,
  `ticker` varchar(10) NOT NULL,
  `company_name` varchar(150) NOT NULL,
  `volume` int(11) NOT NULL,
  `initial_price` float NOT NULL,
  `current_price` float DEFAULT NULL,
  `market_cap` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `stocks`
--

INSERT INTO `stocks` (`id`, `ticker`, `company_name`, `volume`, `initial_price`, `current_price`, `market_cap`) VALUES
(1, 'AAPL', 'Apple Inc.', 5007, 150, 6546.98, 32780700),
(2, 'GOOGL', 'Alphabet Inc.', 30000000, 2800, 2900, 1800000000),
(3, 'AMZN', 'Amazon.com Inc.', 60000000, 3400, 3500, 1700000000),
(4, 'TSLA', 'Tesla Inc.', 70000000, 900, 950, 800000000),
(5, 'MSFT', 'Microsoft Corp.', 80000000, 290, 300, 2200000000),
(7, 'NVDA', 'NVIDIA Corporation', 3434, 1223450, 1223450, 4201340000),
(8, 'NFLX', 'Netflix Inc.', 45345, 6576.67, 3435.45, 155780000),
(9, 'BABA ', 'Alibaba Group Holding Ltd.', 42343, 34543.4, 34543.4, 1462670000);

-- --------------------------------------------------------

--
-- Table structure for table `transactions`
--

CREATE TABLE `transactions` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `order_id` int(11) NOT NULL,
  `transaction_type` varchar(4) NOT NULL,
  `quantity` int(11) NOT NULL,
  `price` float NOT NULL,
  `total` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `transactions`
--

INSERT INTO `transactions` (`id`, `user_id`, `order_id`, `transaction_type`, `quantity`, `price`, `total`) VALUES
(1, 1, 1, 'buy', 50, 150, 7500),
(2, 2, 2, 'buy', 10, 2800, 28000),
(3, 3, 3, 'sell', 5, 3400, 17000),
(4, 4, 4, 'buy', 20, 900, 18000),
(5, 5, 5, 'sell', 100, 290, 29000);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `full_name` varchar(150) NOT NULL,
  `username` varchar(150) NOT NULL,
  `email` varchar(150) NOT NULL,
  `password_hash` varchar(128) NOT NULL,
  `role` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `full_name`, `username`, `email`, `password_hash`, `role`) VALUES
(1, 'John Doe', 'johndoe', 'john@example.com', 'HASHED_PASSWORD_1', 'trader'),
(2, 'Jane Smith', 'janesmith', 'jane@example.com', 'HASHED_PASSWORD_2', 'trader'),
(3, 'Bob Johnson', 'bobjohnson', 'bob@example.com', 'HASHED_PASSWORD_3', 'trader'),
(4, 'Alice Brown', 'alicebrown', 'alice@example.com', 'HASHED_PASSWORD_4', 'trader'),
(5, 'Michael Davis', 'michaeldavis', 'michael@example.com', 'HASHED_PASSWORD_5', 'trader'),
(5555, 'Trader', 'trader', 'trader@test.com', '$2b$12$Oljc0LASZs5bDqUydoNeXuruCpM24DuaID7E8wgBuc88z31dVlRVa', 'trader'),
(7777, 'Admin', 'admin', 'admin@test.com', '$2b$12$vWyGGNCb//MNJN4A8XZy5OF3dm784eQ255nTFu3bRnHShB/0P7RRa', 'admin');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `alembic_version`
--
ALTER TABLE `alembic_version`
  ADD PRIMARY KEY (`version_num`);

--
-- Indexes for table `cash_transactions`
--
ALTER TABLE `cash_transactions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `market_hours`
--
ALTER TABLE `market_hours`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `stock_id` (`stock_id`);

--
-- Indexes for table `portfolios`
--
ALTER TABLE `portfolios`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `portfolio_stocks`
--
ALTER TABLE `portfolio_stocks`
  ADD PRIMARY KEY (`id`),
  ADD KEY `portfolio_id` (`portfolio_id`),
  ADD KEY `stock_id` (`stock_id`);

--
-- Indexes for table `stocks`
--
ALTER TABLE `stocks`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ticker` (`ticker`);

--
-- Indexes for table `transactions`
--
ALTER TABLE `transactions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `order_id` (`order_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `cash_transactions`
--
ALTER TABLE `cash_transactions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `market_hours`
--
ALTER TABLE `market_hours`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `orders`
--
ALTER TABLE `orders`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `portfolios`
--
ALTER TABLE `portfolios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `portfolio_stocks`
--
ALTER TABLE `portfolio_stocks`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `stocks`
--
ALTER TABLE `stocks`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `transactions`
--
ALTER TABLE `transactions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7778;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `cash_transactions`
--
ALTER TABLE `cash_transactions`
  ADD CONSTRAINT `cash_transactions_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `orders`
--
ALTER TABLE `orders`
  ADD CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `orders_ibfk_2` FOREIGN KEY (`stock_id`) REFERENCES `stocks` (`id`);

--
-- Constraints for table `portfolios`
--
ALTER TABLE `portfolios`
  ADD CONSTRAINT `portfolios_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `portfolio_stocks`
--
ALTER TABLE `portfolio_stocks`
  ADD CONSTRAINT `portfolio_stocks_ibfk_1` FOREIGN KEY (`portfolio_id`) REFERENCES `portfolios` (`id`),
  ADD CONSTRAINT `portfolio_stocks_ibfk_2` FOREIGN KEY (`stock_id`) REFERENCES `stocks` (`id`);

--
-- Constraints for table `transactions`
--
ALTER TABLE `transactions`
  ADD CONSTRAINT `transactions_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `transactions_ibfk_2` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
