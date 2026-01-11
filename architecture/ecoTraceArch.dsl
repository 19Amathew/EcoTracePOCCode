workspace "Recycling App" "AI powered recycling assistant" {

    model {
        user = person "User" "A person wanting to recycle an item correctly."
        
        recyclingSystem = softwareSystem "Recycling Assistant System" "Allows users to identify and track recycling." {
            mobileApp = container "Mobile Application" "Provides recycling UI, camera interface, and logic." "React Native / Flutter"
            database = container "Local Database" "Stores user recycling history and tracking data." "SQLite / Room"
            scraper = container "Council Collection Service" "Fetches local council collection schedules on demand." "Python / Beautiful Soup"
        }

        # External Systems
        googleVision = softwareSystem "Google Cloud Vision API" "Extracts labels and text from images." "External AI"
        geminiAI = softwareSystem "Gemini AI" "Categorises materials and provides disposal advice." "Generative AI"
        councilWebsites = softwareSystem "Local Council Websites" "Host official council collection schedules." "External Web"

        # Relationships
        user -> mobileApp "Takes photo and views results"
        
        mobileApp -> googleVision "Sends image for object/label detection"
        googleVision -> mobileApp "Returns labels (e.g., 'Plastic Bottle')"
        
        mobileApp -> geminiAI "Sends labels for intelligent categorisation"
        geminiAI -> mobileApp "Returns category and advice (e.g., 'Type 1 PET')"
        
        mobileApp -> database "Stores and retrieves recycling history"
        
        mobileApp -> scraper "Requests local collection schedule"
        scraper -> councilWebsites "Retrieves collection schedule data"
        scraper -> mobileApp "Returns collection schedule"
    }

    views {
        container recyclingSystem "Containers" {
            include *
        }

        styles {
            element "Container" {
                background #438dd5
                color #ffffff
            }
            element "External AI" {
                background #999999
                color #ffffff
            }
        }
    }
}
