DROP TABLE IF EXISTS Loans;
DROP TABLE IF EXISTS LoanProposals;
DROP TABLE IF EXISTS LibraryBooks;
DROP TABLE IF EXISTS Libraries;
DROP TABLE IF EXISTS Books;
DROP TABLE IF EXISTS Users;

CREATE TABLE Users (
    UserCode SERIAL PRIMARY KEY,
    ID VARCHAR(20) NOT NULL,
    Password VARCHAR(20) NOT NULL,
    AuthorCode SMALLINT NOT NULL CHECK (AuthorCode IN (0, 1, 2)),
    LibCode INT,
    Name VARCHAR(100) NOT NULL,
    Age INT,
    Gender VARCHAR(1) CHECK (Gender IN ('M', 'F')) NOT NULL,
    PhoneNumber VARCHAR(15),
    Email VARCHAR(100),
    CHECK (AuthorCode <> 1 OR LibCode IS NOT NULL)  -- 도서관 관리자의 경우에만 LibCode가 NULL이 아님
);

CREATE TABLE Books (
    ISBN CHAR(13) PRIMARY KEY,
    BookName VARCHAR(255) NOT NULL,
    Authors VARCHAR(100) NOT NULL,
    Publisher VARCHAR(100),
    PublicationYear INT CHECK (PublicationYear > 0),
    ClassNm VARCHAR(20),
    ClassNo VARCHAR(255)
);

CREATE TABLE Libraries (
    LibCode INT PRIMARY KEY,
    LibName VARCHAR(255) NOT NULL,
    Address VARCHAR(255) NOT NULL,
    Tel VARCHAR(30),
    Fax VARCHAR(30),
    Latitude DECIMAL(9, 6),
    Longitude DECIMAL(9, 6),
    Homepage VARCHAR(255),
    Closed BOOLEAN NOT NULL DEFAULT FALSE,
    OperatingTime VARCHAR(500),
    BookCount INT DEFAULT 0
);

CREATE TABLE LibraryBooks (
    LibCode INT REFERENCES Libraries(LibCode) ON DELETE CASCADE ON UPDATE CASCADE,
    ISBN CHAR(13) REFERENCES Books(ISBN) ON DELETE CASCADE ON UPDATE CASCADE,
    Vol VARCHAR(5),
    CallNumber VARCHAR(100) NOT NULL,
    RegistrationDate DATE NOT NULL DEFAULT CURRENT_DATE,
    ISLoan BOOLEAN NOT NULL DEFAULT FALSE,
    PRIMARY KEY (LibCode, ISBN, Vol, CallNumber)
);

CREATE TABLE LoanProposals (
    ProposalID SERIAL PRIMARY KEY,
    LibCode INT NOT NULL,
    ISBN CHAR(13) NOT NULL,
    Vol VARCHAR(10) NOT NULL,
    CallNumber VARCHAR(100) NOT NULL,
    UserCode INT NOT NULL,
    LoanClassification INT NOT NULL,             -- 대출 분류 (예: 0: 대출 신청, 1: 빈납 신청)
    FOREIGN KEY (LibCode, ISBN, Vol, CallNumber) REFERENCES LibraryBooks(LibCode, ISBN, Vol, CallNumber) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (ISBN) REFERENCES Books(ISBN) ON DELETE CASCADE ON UPDATE CASCADE  -- Books에 대한 외래 키
);

CREATE TABLE Loans (
    LoanCode SERIAL PRIMARY KEY,
    LibCode INT REFERENCES Libraries(LibCode) ON DELETE CASCADE ON UPDATE CASCADE,
    ISBN CHAR(13) NOT NULL,
    Vol VARCHAR(10) NOT NULL,
    CallNumber VARCHAR(100) NOT NULL,
    UserCode INT REFERENCES Users(UserCode) ON DELETE CASCADE ON UPDATE CASCADE,
    LoanDate DATE NOT NULL DEFAULT CURRENT_DATE,        -- 대출 시작 날짜
    ReturnDate DATE,                                    -- 대출 시작 날짜 + 14
    LoanExtensions INT DEFAULT 0,
    FOREIGN KEY (LibCode, ISBN, Vol, CallNumber) REFERENCES LibraryBooks(LibCode, ISBN, Vol, CallNumber) ON DELETE CASCADE ON UPDATE CASCADE
);

INSERT INTO Users (ID, Password, AuthorCode, LibCode, Name, Age, Gender, PhoneNumber, Email)
VALUES ('user123', 'password123', 0, NULL, 'John Doe', 30, 'M', '123-456-7890', 'john.doe@example.com');
