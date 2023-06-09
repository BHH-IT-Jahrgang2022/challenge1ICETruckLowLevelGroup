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
        tempSet--;
        updateTempSetView();
    }

    private void pluTempBtn_Clicked(object sender, EventArgs e)
    {
        tempSet++;
        updateTempSetView();
    }

    private void updateTempSetView()
    {
        lblTempSet.Text = $"{tempSet}°C";
    }
}

