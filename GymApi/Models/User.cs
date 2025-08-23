using System.ComponentModel.DataAnnotations;

namespace GymApi.Models {
  public class User
  {
    public string? firstName { get; set; }
    public string? lastName { get; set; }
    public string? email { get; set; }
    public string? passwordHash { get; set; }
    public bool? isActive { get; set; }
    public System.DateOnly? joinDate { get; set; }
    public int? weight { get; set; }
    public int? height { get; set; }
    public int? age { get; set; }
    public string? gender { get; set; }
    public string? profilePictureUrl { get; set; }
  }
}