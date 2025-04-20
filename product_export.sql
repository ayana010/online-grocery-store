PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT,
    unit_price REAL,
    unit_quantity TEXT,
    in_stock INTEGER
, category TEXT, image_url TEXT);
INSERT INTO products VALUES(1000,'Fish Fingers',2.5499999999999998223,'500 gram',1498,'Frozen','https://via.placeholder.com/100x100?text=Fish');
INSERT INTO products VALUES(1001,'Fish Fingers',5.0,'1000 gram',748,'Frozen',NULL);
INSERT INTO products VALUES(1002,'Hamburger Patties',2.3500000000000000888,'Pack 10',1199,'Frozen',NULL);
INSERT INTO products VALUES(1003,'Shelled Prawns',6.9000000000000003552,'250 gram',300,'Frozen',NULL);
INSERT INTO products VALUES(1004,'Tub Ice Cream',1.8,'1 Litre',799,'Frozen','https://via.placeholder.com/100x100?text=Ice+Cream');
INSERT INTO products VALUES(1005,'Tub Ice Cream',3.3999999999999999111,'2 Litre',1199,'Frozen',NULL);
INSERT INTO products VALUES(2000,'Panadol',3.0,'Pack 24',2000,'Health',NULL);
INSERT INTO products VALUES(2001,'Panadol',5.5,'Bottle 50',999,'Health',NULL);
INSERT INTO products VALUES(2002,'Bath Soap',2.6000000000000000888,'Pack 6',500,'Household',NULL);
INSERT INTO products VALUES(2003,'Garbage Bags Small',1.5,'Pack 10',499,'Household',NULL);
INSERT INTO products VALUES(2004,'Garbage Bags Large',5.0,'Pack 50',299,'Household',NULL);
INSERT INTO products VALUES(2005,'Washing Powder',4.0,'1000 gram',800,'Household',NULL);
INSERT INTO products VALUES(2006,'Laundry Bleach',3.5499999999999998223,replace('2 Litre \nBottle','\n',char(10)),500,'Health',NULL);
INSERT INTO products VALUES(3000,'Cheddar Cheese',8.0,'500 gram',1000,'Dairy',NULL);
INSERT INTO products VALUES(3001,'Cheddar Cheese',15.0,'1000 gram',998,'Dairy',NULL);
INSERT INTO products VALUES(3002,'T Bone Steak',7.0,'1000 gram',200,'Meat & Produce',NULL);
INSERT INTO products VALUES(3003,'Navel Oranges',3.9900000000000002131,'Bag 20',200,'Meat & Produce',NULL);
INSERT INTO products VALUES(3004,'Bananas',1.4900000000000000355,'Kilo',400,'Meat & Produce',NULL);
INSERT INTO products VALUES(3005,'Peaches',2.9900000000000002131,'Kilo',500,'Meat & Produce',NULL);
INSERT INTO products VALUES(3006,'Grapes',3.5,'Kilo',200,'Meat & Produce',NULL);
INSERT INTO products VALUES(3007,'Apples',1.9900000000000000355,'Kilo',500,'Meat & Produce',NULL);
INSERT INTO products VALUES(4000,'Earl Grey Tea Bags',2.4900000000000002131,'Pack 25',1200,'Beverages','https://via.placeholder.com/100x100?text=Tea');
INSERT INTO products VALUES(4001,'Earl Grey Tea Bags',7.25,'Pack 100',1200,'Beverages',NULL);
INSERT INTO products VALUES(4002,'Earl Grey Tea Bags',13.0,replace('Pack \n200','\n',char(10)),800,'Beverages',NULL);
INSERT INTO products VALUES(4003,'Instant Coffee',2.8900000000000002131,'200 gram',500,'Beverages',NULL);
INSERT INTO products VALUES(4004,'Instant Coffee',5.0999999999999996447,'500 gram',500,'Beverages',NULL);
INSERT INTO products VALUES(4005,'Chocolate Bar',2.5,'500 gram',300,'Beverages',NULL);
INSERT INTO products VALUES(5000,'Dry Dog Food',5.9500000000000001776,'5 kg Pack',400,'Pet Food',NULL);
INSERT INTO products VALUES(5001,'Dry Dog Food',1.95,'1 kg Pack',399,'Pet Food',NULL);
INSERT INTO products VALUES(5002,'Bird Food',3.9900000000000002131,'500g packet',200,'Pet Food',NULL);
INSERT INTO products VALUES(5003,'Cat Food',2.0,'500g tin',200,'Pet Food',NULL);
INSERT INTO products VALUES(5004,'Fish Food',3.0,'500g packet',200,'Pet Food',NULL);
COMMIT;
