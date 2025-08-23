using Microsoft.AspNetCore.Mvc;
using GymApi.Services;
using GymApi.Models;

namespace GymApi.Controllers;

[ApiController]
[Route("[controller]")]
public class UserController : ControllerBase {
    
    private readonly UserService _service;
    public UserController(UserService service) { _service = service; }
    
  // Creates user in db, responds with refresh and access tokens if successful request.
  [HttpPost("create")]
  public IActionResult Create([FromBody] User user) {
      if (!ModelState.IsValid) { return BadRequest(ModelState); }
      _service.CreateUser(user);
        
      
      
      return Ok("User Created Successfully");
  }

  // Updates user in db.
  [HttpPost("update")]
  public IActionResult Update([FromBody] User user) {
    if (!ModelState.IsValid) { return BadRequest(ModelState); }
    

    return Ok("User Updated Successfully");
  }


}