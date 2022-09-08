import React, { useState, useEffect } from 'react';
import Modal from 'react-modal';
/**
 * book edit form 
 * @param {*} param0 the bookEdit function, and currentBook is the book to edit 
 */
function BookEdit({bookEdit, currentBook}) {
    const [modalIsOpen, setIsOpen] = useState(false); 
    const [book, setBook] = useState(currentBook); 
    
    function openModal() {
        setIsOpen(true);
    }

    function closeModal(){
        setIsOpen(false);
    }

    return (
        <div>
          <button className="btn btn-outline-info btn-block" onClick={openModal}>Edit</button>
            <Modal 
                isOpen={modalIsOpen}
                contentLabel="Book Edit"
                onRequestClose={closeModal}
            >
                    <form className="border p-3">
                    <div class="form-row">
                        <div className="form-group col-md-6">
                            <label for="bookTitle">Title</label>
                            <input type="text" className="form-control" id="bookTitle" defaultValue={currentBook.title}
                            onChange={e => setBook({...book, title: e.target.value})}></input>
                        </div>
                        <div className="form-group col-md-6">
                            <label for="bookURL">Book URL</label>
                            <input type="text" className="form-control" id="bookURL" defaultValue={currentBook.book_url}
                            onChange={e => setBook({...book, book_url: e.target.value})}></input>
                        </div>
                    </div>
                    <div class="form-row">
                        <div className="form-group col-md-6">
                            <label for="bookISBN">ISBN</label>
                            <input type="text" className="form-control" id="bookISBN" defaultValue={currentBook.ISBN}
                            onChange={e => setBook({...book, ISBN: e.target.value})}></input>
                        </div>
                        <div className="form-group col-md-6">
                            <label for="bookImg">Image URL</label>
                            <input type="text" className="form-control" id="bookImg" defaultValue={currentBook.image_url}
                            onChange={e => setBook({...book, image_url: e.target.value})}></input>
                        </div>
                    </div>
                    <div class="form-row">
                        <div className="form-group col-md-6">
                            <label for="bookAuthor">Author</label>
                            <input type="text" className="form-control" id="bookAuthor" defaultValue={currentBook.author}
                            onChange={e => setBook({...book, author: e.target.value})}></input>
                        </div>
                        <div className="form-group col-md-6">
                            <label for="bookAuthorURL">Author URL</label>
                            <input type="text" className="form-control" id="bookAuthorURL" defaultValue={currentBook.author_url}
                            onChange={e => setBook({...book, author_url: e.target.value})}></input>
                        </div>
                    </div>
                    <div class="form-row">
                        <div className="form-group col-md-4">
                            <label for="bookRating">Rating</label>
                            <input type="text" className="form-control" id="bookRating" defaultValue={currentBook.rating}
                            onChange={e => setBook({...book, rating: e.target.value})}></input>
                        </div>
                        <div className="form-group col-md-4">
                            <label for="bookRatingCount">Rating Count</label>
                            <input type="text" className="form-control" id="bookRatingCount" defaultValue={currentBook.rating_count}
                            onChange={e => setBook({...book, rating_count: e.target.value})}></input>
                        </div>
                        <div className="form-group col-md-4">
                            <label for="bookReviewCount">Review Count</label>
                            <input type="text" className="form-control" id="bookReviewCount" defaultValue={currentBook.review_count}
                            onChange={e => setBook({...book, review_count: e.target.value})}></input>
                        </div>
                    </div>
                    <div className="form-row">
                        <div className="form-group col-md-6">
                            <button type="button" className="btn btn-outline-info btn-block" id="bookEdit" onClick={() => {bookEdit(book); closeModal();}}>Edit</button>
                        </div>
                        <div className="form-group col-md-6">
                            <button type="button" className="btn btn-outline-danger btn-block" id="cancel" onClick={() => {closeModal();}}>Cancel</button>
                        </div>
                    </div>
                    </form>

                
            </Modal>
        </div>
    ); 
}

export default BookEdit;
