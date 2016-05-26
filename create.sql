CREATE TABLE IF NOT EXISTS `iask_answers` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Auto-increment ID',
  `text` text NOT NULL COMMENT 'Answer content',
  `question_id` int(18) NOT NULL COMMENT 'Question ID',
  `author` varchar(255) NOT NULL COMMENT 'Author',
  `is_good` int(11) NOT NULL COMMENT 'Is good or not',
  PRIMARY KEY(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `iask_questions` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Auto-increment ID',
  `text` text NOT NULL COMMENT 'Question content',
  `qauthor` varchar(255) NOT NULL COMMENT 'Question Author',
  `url` varchar(255) NOT NULL COMMENT 'Question URL',
  PRIMARY KEY(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
