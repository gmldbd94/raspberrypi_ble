from bleson import get_provider, Advertiser, Advertisement

def stopadvertising():
    adapter = get_provider().get_adapter()
    advertiser = Advertiser(adapter)
    advertisement = Advertisement()
    advertiser.advertisement = advertisement
    advertiser.stop()
    
###MAIN###
stopadvertising()
print("ADVERTISING STOP!")