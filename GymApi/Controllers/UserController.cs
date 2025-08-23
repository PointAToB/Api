using Microsoft.AspNetCore.Mvc;

namespace GymApi.Controllers;

[ApiController]
[Route("[controller]")]
public class UserController : ControllerBase {

  [HttpPost(Name="create_user")]
  public IActionResult Post([FromBody] User user) {
      if (!ModelState.IsValid) { return BadRequest(ModelState); }

      return Ok("User Created Successfully");
  }


}