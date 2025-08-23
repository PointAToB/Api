using MongoDB.Driver;
using GymApi.Models;
using Microsoft.AspNetCore.Identity;


namespace GymApi.Services {
    public class UserService {

        private readonly IMongoCollection<User> _collection;
        private readonly IPasswordHasher<User> _passwordHasher;
        
        public UserService(IMongoClient client, IPasswordHasher<User> passwordHasher) {
            var db = client.GetDatabase("Gym-Api");
            _collection = db.GetCollection<User>("Users");
            _passwordHasher = passwordHasher;
        }

        // Creates user adds to Users table
        public void CreateUser(User user) {
            if (user.passwordHash == null) { return; }
            
            // Hashes password
            user.passwordHash = _passwordHasher.HashPassword(user, user.passwordHash); 

            _collection.InsertOne(user);
        }
    }
}
