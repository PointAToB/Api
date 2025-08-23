using System;
using System.ComponentModel.DataAnnotations;
public class User {
  public long userId { get; set; }
  [Required]
  public string firstName { get; set; }
  [Required]
  public string lastName { get; set; }
  [Required]
  public string email { get; set; }
  [Required]
  public string password { get; set; }
  public bool isActive { get; set; }
  public System.DateOnly joinDate { get; set; }
  public int weight { get; set; }
  public int height { get; set; }
  public int age { get; set; }
  public string gender { get; set; }
  public string profilePictureUrl { get; set; }
}