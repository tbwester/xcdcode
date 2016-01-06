///////////////////////////////////////////
// Thomas Wester
// University of Chicago
// Autumn 2015
// Usage: Run script with darkroot libraries.
//        Gets laser histograms from files
//        listed in runlist.txt
//        Make sure the files exist and have
//        laser histograms in them.
//        Individual histograms are outputted to
//        "hist" folder for checking fits
///////////////////////////////////////////

#include"TFile.h"
#include"TMultiGraph.h"
#include"TLine.h"
#include"TGraph.h"
#include"TGraphErrors.h"
#include"TCanvas.h"
#include"TPad.h"
#include"TPaveText.h"
#include"TAxis.h"
#include"TMath.h"
#include"TStyle.h"
#include"TFrame.h"
#include"TLegend.h"
#include"TH1F.h"
#include"TF1.h"

#include<string>
#include<vector>
#include<sstream>
#include<fstream>
#include<iomanip>

using namespace std;

string toString(double d);
void singlepe() {

  TCanvas *c1 = new TCanvas("c1","c1",1000,800);
 
  TPad *pad1 = new TPad("pad1", "ch0", 0.01, 0.99, 0.01, 0.99);
  pad1->SetFillColor(18);
  c1->cd();
  pad1->Draw();

  ifstream fin;
  fin.open("runlist.txt");

  vector<float> x;
  vector<float> y;
  vector<float> xerr;
  vector<float> yerr;
    
  //Read in each line of the runlist.txt file.
  int runCounter = 0;
  string RunName;
  while (fin >> RunName) {
      
    x.push_back(runCounter); //("Run" + RunName);    
    xerr.push_back(0.);

    //Create a string for the run's root file.
    string filepath = "/data/xcd/processed/v1_0_1/";
    string filename = filepath + "Run" + RunName + ".root";
    
    cout << filename.c_str() << endl;

    //Extract the plot from the run's root file.
    TFile *f1 = TFile::Open(filename.c_str());
    TH1D *h1 = (TH1D *)f1->Get("channel_0_laser_int_hist");

    int peakWidth = 20;
    int peakCenter = 130;

    TF1* mygaus = new TF1("mygaus","[0]*TMath::Exp(-0.5*((x-[1])/[2])^2)",
                          peakCenter - peakWidth, peakCenter + peakWidth);
    
    mygaus->SetParameter(0,1);
    mygaus->SetParameter(1, peakCenter);
    mygaus->SetParameter(2, 80);

    h1->Fit("mygaus","R","",peakCenter - peakWidth, peakCenter + peakWidth);
    string outfile = "hist/" + RunName + ".root";
    TFile f(outfile.c_str(),"RECREATE");
    h1->Write(RunName.c_str());
    
    TF1 *myfit = (TF1 *)h1->GetFunction("mygaus");
    y.push_back(myfit->GetParameter(1));
    yerr.push_back(myfit->GetParError(1));  

    runCounter++;
  }

  fin.close();

  TGraphErrors *gr = new TGraphErrors(x.size(), &(x[0]), &(y[0]), 
                                                &(xerr[0]), &(yerr[0]));

  int xmin = *min_element(x.begin(),x.end());
  int xmax = *max_element(x.begin(),x.end());

  TF1* flat = new TF1("flat","[0]", xmin, xmax);
  flat->SetParameter(0,gr->GetMean(2));
 
  gr->Fit("flat","R","", xmin, xmax);
  TF1 *flatfit = (TF1 *)gr->GetFunction("flat");

  double rcs = flatfit->GetChisquare() / flatfit->GetNDF();

  fin.open("runlist.txt");
  int PointCounter = 0; //Stores the number of points to plot
  while (fin >> RunName) {
      int bin_index = gr->GetXaxis()->FindBin(x[PointCounter]);
      gr->GetXaxis()->SetBinLabel(bin_index, RunName.c_str());
      PointCounter++;
  }
  fin.close();
  
  gStyle->SetOptStat(1011);

  gr->GetXaxis()->SetLabelSize(0.02);
  gr->GetXaxis()->LabelsOption("v");
  gr->GetXaxis()->SetTitle("Run #");
  gr->GetXaxis()->CenterTitle();
  gr->GetYaxis()->SetTitle("Peak Position (Count*Samples)");
  gr->GetYaxis()->CenterTitle();

  gr->GetXaxis()->SetRangeUser(xmin - 1, xmax + 1);

  gr->SetTitle("Single PE Peak Positions");
  gr->SetMarkerColor(1);
  gr->SetMarkerStyle(7);
  gr->Draw("AP");

  TLine *line = new TLine(xmin, gr->GetMean(2), xmax, gr->GetMean(2));
  line->SetLineWidth(2);
  line->SetLineColor(4);
  line->Draw();

  TPaveText *pt = new TPaveText(.05,.7,.25,.8,"brNDC");
  string meanStr = "Mean: " + toString(gr->GetMean(2));
  string rmsStr = "RMS: " + toString(gr->GetRMS(2));
  string chsqStr = "rChsq: " + toString(flatfit->GetChisquare()) + " / " +
                   toString(flatfit->GetNDF()) + " = " + toString(rcs);
  pt->AddText(meanStr.c_str());
  pt->AddText(rmsStr.c_str());
  pt->AddText(chsqStr.c_str());
  pt->Draw();

  TLegend* leg = new TLegend(0.45,0.8,0.65,0.88);
  leg->SetHeader("Legend");
  leg->AddEntry("gr","SPE Peak Data","ep");
  leg->AddEntry(line,"Mean","l");
  leg->AddEntry(flatfit, "Fit", "l");
  leg->Draw();

  cout << gr->GetMean(2) << ", " << gr->GetRMS(2) << endl;
}

string toString(double d) {
  stringstream ss;
  ss << d;
  return ss.str();
}
