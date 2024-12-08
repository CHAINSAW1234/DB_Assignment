-- LibraryBooks에 데이터 삽입 시 BookCount 업데이트
CREATE OR REPLACE FUNCTION update_book_count_after_insert()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE Libraries
    SET BookCount = (SELECT COUNT(*)
                     FROM LibraryBooks
                     WHERE LibCode = NEW.LibCode)
    WHERE LibCode = NEW.LibCode;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER after_librarybook_insert
AFTER INSERT ON LibraryBooks
FOR EACH ROW
EXECUTE FUNCTION update_book_count_after_insert();

-- LibraryBooks에서 데이터 삭제 시 BookCount 업데이트
CREATE OR REPLACE FUNCTION update_book_count_after_delete()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE Libraries
    SET BookCount = (SELECT COUNT(*)
                     FROM LibraryBooks
                     WHERE LibCode = OLD.LibCode)
    WHERE LibCode = OLD.LibCode;
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER after_librarybook_delete
AFTER DELETE ON LibraryBooks
FOR EACH ROW
EXECUTE FUNCTION update_book_count_after_delete();

-- Loans 테이블에 데이터 삽입 시 ISLoan 업데이트
CREATE OR REPLACE FUNCTION update_isloan_after_insert()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE LibraryBooks
    SET ISLoan = EXISTS (
        SELECT 1 FROM Loans
        WHERE LibCode = NEW.LibCode
        AND ISBN = NEW.ISBN
        AND Vol = NEW.Vol
        AND CallNumber = NEW.CallNumber
    )
    WHERE LibCode = NEW.LibCode
    AND ISBN = NEW.ISBN
    AND Vol = NEW.Vol
    AND CallNumber = NEW.CallNumber;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER after_loan_insert
AFTER INSERT ON Loans
FOR EACH ROW
EXECUTE FUNCTION update_isloan_after_insert();

-- 대출 삭제 후 ISLoan 업데이트 함수
CREATE OR REPLACE FUNCTION update_isloan_after_delete()
RETURNS TRIGGER AS $$
BEGIN
    -- 대출이 삭제된 후, 해당 책이 더 이상 대출 중이지 않은지 확인
    UPDATE LibraryBooks
    SET ISLoan = CASE
        WHEN EXISTS (
            SELECT 1 FROM Loans
            WHERE LibCode = OLD.LibCode
            AND ISBN = OLD.ISBN
            AND Vol = OLD.Vol
            AND CallNumber = OLD.CallNumber
        ) THEN TRUE
        ELSE FALSE
    END
    WHERE LibCode = OLD.LibCode
    AND ISBN = OLD.ISBN
    AND Vol = OLD.Vol
    AND CallNumber = OLD.CallNumber;

    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

-- 대출 삭제 트리거 생성
CREATE TRIGGER after_loan_deletion
AFTER DELETE ON Loans
FOR EACH ROW
EXECUTE FUNCTION update_isloan_after_delete();
