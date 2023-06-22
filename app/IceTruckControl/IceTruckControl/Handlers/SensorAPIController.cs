using System;
using System.Net.Http;

using IceTruckControl.Models;

namespace IceTruckControl.Handlers
{
	public static class SensorAPIController
	{

		static readonly string BaseAddress = "https://api.azubilab.cc";
		static readonly string Url = $"{BaseAddress}/";

		private static HttpClient client;
		


		public static async Task<IEnumerable<Sensor>> GetAllTemps() {
			// Check if connected

			if (Connectivity.Current.NetworkAccess != NetworkAccess.Internet)
				return new List<Sensor>();

			throw new NotImplementedException();
		}

		public static async Task<Sensor> GetAllTempFromSense(int SenseId) {
			throw new NotImplementedException();
		}
	}
}

