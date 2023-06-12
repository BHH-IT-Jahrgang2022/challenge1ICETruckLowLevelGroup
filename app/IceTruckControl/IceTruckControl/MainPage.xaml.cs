using System.Diagnostics;

namespace IceTruckControl;

public partial class MainPage : ContentPage
{

	int tempSet = -17; // just a temp value thats not possible
	public MainPage()
	{
		InitializeComponent();
	}

    protected override void OnAppearing()
    {
        base.OnAppearing();
        updateTempSetView();
    }


    private void minTempBtn_Clicked(object sender, EventArgs e)
    {
        if (tempSet > -40)
        {
            tempSet--;
            updateTempSetView();
        } else if (tempSet > -273.15) {
            Debug.WriteLine("ERROR: This value is not possible for the hardware");
            DisplayAlert("Temp not possible", "Due to Hardware limitations, please stick to a temperature greater than -40", "ok");
        }
        else 
        {
            DisplayAlert("PHYSICS BROKE NOW", 
                        "Hey! Stop breaking physics! It's not possible to cool something under the physical limit! You noop!", 
                        "Physics does not count for me!");
        }
        
    }

    private void pluTempBtn_Clicked(object sender, EventArgs e)
    {
        if (tempSet < 80) 
        {
            tempSet++;
            updateTempSetView();
        } else 
        {
            Debug.WriteLine("ERROR: This value literally is not possible");
            DisplayAlert("Temp not possible", "Due to Hardware limitations, please stick to a temperature smaller than 80", "ok");
        }
        
    }

    private void updateTempSetView()
    {
        lblTempSet.Text = $"{tempSet}°C";
    }
}

