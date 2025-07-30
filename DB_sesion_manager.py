from sqlalchemy.exc import SQLAlchemyError
import logging


class DBSessionManager:
    def __init__(self, session_factory):
        self.session_factory = session_factory
        self.session = None

    def __enter__(self):
        """Enter the runtime context - create session"""
        self.session = self.session_factory()
        return self.session

    def __exit__(self, exc_type, exc_value, traceback):
        """Exit the context - handle commit/rollback"""
        if self.session:
            if exc_type:  # Exception occurred in with-block
                self.session.rollback()
                logging.error("Transaction rolled back due to error")
            else:  # No exception - try to commit
                try:
                    self.session.commit()
                except SQLAlchemyError:
                    self.session.rollback()
                    logging.error("Commit failed, rolled back")
                    raise  # Re-raise for custom handling
            self.session.close()
