import React, { useState, useEffect } from 'react';
import Modal from 'react-modal';
/**
 * the author edit form 
 * @param {*} param0 the authorEdit function, and currentAuthor is the book to edit 
 */
function AuthorEdit({authorEdit, currentAuthor}) {
    const [modalIsOpen, setIsOpen] = useState(false); 
    const [author, setAuthor] = useState(currentAuthor); 
    
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
                contentLabel="author Edit"
                onRequestClose={closeModal}
            >
                Name Author URL Image URL 
                    <form className="border p-3">
                    <div class="form-row">
                        <div className="form-group col-md-4">
                            <label for="authorName">Name</label>
                            <input type="text" className="form-control" id="authorName" defaultValue={currentAuthor.name}
                            onChange={e => setAuthor({...author, name: e.target.value})}></input>
                        </div>
                        <div className="form-group col-md-4">
                            <label for="authorURL">Author URL</label>
                            <input type="text" className="form-control" id="authorURL" defaultValue={currentAuthor.author_url}
                            onChange={e => setAuthor({...author, author_url: e.target.value})}></input>
                        </div>
                        <div className="form-group col-md-4">
                            <label for="authorImg">Image URL</label>
                            <input type="text" className="form-control" id="authorImg" defaultValue={currentAuthor.image_url}
                            onChange={e => setAuthor({...author, image_url: e.target.value})}></input>
                        </div>
                    </div>
                    <div class="form-row">
                        <div className="form-group col-md-4">
                            <label for="authorRating">Rating</label>
                            <input type="text" className="form-control" id="authorRating" defaultValue={currentAuthor.rating}
                            onChange={e => setAuthor({...author, rating: e.target.value})}></input>
                        </div>
                        <div className="form-group col-md-4">
                            <label for="authorRatingCount">Rating Count</label>
                            <input type="text" className="form-control" id="authorRatingCount" defaultValue={currentAuthor.rating_count}
                            onChange={e => setAuthor({...author, rating_count: e.target.value})}></input>
                        </div>
                        <div className="form-group col-md-4">
                            <label for="authorReviewCount">Review Count</label>
                            <input type="text" className="form-control" id="authorReviewCount" defaultValue={currentAuthor.review_count}
                            onChange={e => setAuthor({...author, review_count: e.target.value})}></input>
                        </div>
                    </div>
                    <div className="form-row">
                        <div className="form-group col-md-6">
                            <button type="button" className="btn btn-outline-info btn-block" id="authorEdit" onClick={() => {authorEdit(author); closeModal();}}>Edit</button>
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

export default AuthorEdit;